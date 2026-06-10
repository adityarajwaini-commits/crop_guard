import os
import time
import torch
import numpy as np
import onnxruntime as ort
from config import Config
from models.train import build_model

def export_model_to_onnx(pytorch_model_path: str, onnx_model_path: str):
    """
    Loads PyTorch checkpoint and exports the model structure to an ONNX file.
    """
    logging_info("Loading PyTorch model for export...")
    # Determine device (CPU for export validation and standard benchmarking)
    device = torch.device("cpu")
    
    if not os.path.exists(pytorch_model_path):
        raise FileNotFoundError(f"PyTorch model checkpoint not found at: {pytorch_model_path}")
        
    checkpoint = torch.load(pytorch_model_path, map_location=device)
    class_names = checkpoint['class_names']
    num_classes = len(class_names)
    
    # Rebuild model and load state
    model = build_model(num_classes=num_classes, freeze_backbone=False)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
    # Create dummy input matching training image dimensions (BCHW)
    dummy_input = torch.randn(1, 3, Config.IMAGE_SIZE[0], Config.IMAGE_SIZE[1], requires_grad=True)
    
    # Export the model
    os.makedirs(os.path.dirname(onnx_model_path), exist_ok=True)
    print(f"Exporting model to ONNX at {onnx_model_path}...")
    torch.onnx.export(
        model,
        dummy_input,
        onnx_model_path,
        export_params=True,
        opset_version=12,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}
    )
    # Save class names list to class_names.txt
    class_names_path = os.path.join(os.path.dirname(onnx_model_path), "class_names.txt")
    print(f"Saving class names to {class_names_path}...")
    with open(class_names_path, "w", encoding="utf-8") as f:
        for name in class_names:
            f.write(f"{name}\n")

    print("ONNX model export complete.")
    return model, dummy_input, class_names

def validate_and_benchmark(pytorch_model, dummy_input, onnx_model_path, num_runs=100):
    """
    Validates output matching between PyTorch and ONNX Runtime, and benchmarks latency.
    """
    # 1. Load ONNX Runtime session
    ort_session = ort.InferenceSession(onnx_model_path, providers=['CPUExecutionProvider'])
    input_name = ort_session.get_inputs()[0].name
    
    # Convert dummy tensor to numpy format
    dummy_input_numpy = dummy_input.detach().numpy()
    
    # 2. Validation Check
    print("Validating model prediction accuracy...")
    with torch.no_grad():
        py_outputs = pytorch_model(dummy_input).numpy()
        
    ort_inputs = {input_name: dummy_input_numpy}
    ort_outputs = ort_session.run(None, ort_inputs)[0]
    
    # Compare raw outputs within narrow floating point bounds
    try:
        np.testing.assert_allclose(py_outputs, ort_outputs, rtol=1e-03, atol=1e-05)
        print("Validation PASSED: PyTorch and ONNX outputs match perfectly!")
    except AssertionError as e:
        print(f"Validation FAILED: Outputs differ. Details:\n{e}")
        return

    # 3. Latency Benchmarking
    print(f"Benchmarking latency over {num_runs} runs...")
    
    # Warmup runs
    for _ in range(10):
        with torch.no_grad():
            _ = pytorch_model(dummy_input)
        _ = ort_session.run(None, ort_inputs)

    # PyTorch Benchmarking
    py_times = []
    for _ in range(num_runs):
        start = time.perf_counter()
        with torch.no_grad():
            _ = pytorch_model(dummy_input)
        py_times.append(time.perf_counter() - start)
        
    # ONNX Benchmarking
    ort_times = []
    for _ in range(num_runs):
        start = time.perf_counter()
        _ = ort_session.run(None, ort_inputs)
        ort_times.append(time.perf_counter() - start)

    py_mean = np.mean(py_times) * 1000  # Convert to milliseconds
    ort_mean = np.mean(ort_times) * 1000
    
    speedup = py_mean / ort_mean

    print("\n" + "="*50)
    print("              Inference Latency Comparison")
    print("="*50)
    print(f"PyTorch CPU Avg Latency: {py_mean:.2f} ms")
    print(f"ONNX CPU Avg Latency:    {ort_mean:.2f} ms")
    print(f"Performance Speedup:     {speedup:.2f}x faster with ONNX")
    print("="*50 + "\n")

def logging_info(msg):
    print(f"[INFO] {msg}")

if __name__ == "__main__":
    pytorch_path = os.path.join(Config.SAVED_MODELS_DIR, "best_model.pth")
    if not os.path.exists(pytorch_path):
        pytorch_path = os.path.join(Config.SAVED_MODELS_DIR, "best_head_model.pth")
        
    onnx_path = os.path.join(Config.SAVED_MODELS_DIR, "model.onnx")
    
    try:
        py_model, dummy, classes = export_model_to_onnx(pytorch_path, onnx_path)
        validate_and_benchmark(py_model, dummy, onnx_path)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        print("Please train your model first using python -m models.train before exporting to ONNX.")
