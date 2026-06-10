"""
Evaluate the Phase 1 head-only checkpoint on the test set and export to ONNX.
"""
import os
import sys
import torch
import torch.nn as nn
import json
import logging
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def build_model(num_classes: int, freeze_backbone: bool = True) -> nn.Module:
    """Builds ResNet-50 model with custom classification head."""
    import torchvision.models as models
    from torchvision.models import ResNet50_Weights
    
    logging.info(f"Loading pretrained ResNet-50 backbone...")
    weights = ResNet50_Weights.DEFAULT
    model = models.resnet50(weights=weights)

    if freeze_backbone:
        logging.info("Freezing ResNet-50 backbone layers...")
        for param in model.parameters():
            param.requires_grad = False
            
    # Replace classification layer
    in_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Linear(in_features, 512),
        nn.ReLU(),
        nn.Dropout(0.3),
        nn.Linear(512, num_classes)
    )
    logging.info(f"Replaced classifier head with custom classification head for {num_classes} classes.")
    return model

def evaluate(model, loader, criterion, device):
    """Evaluates model on a dataset."""
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)

            running_loss += loss.item() * images.size(0)
            _, preds = torch.max(outputs, 1)
            correct += torch.sum(preds == labels.data).item()
            total += labels.size(0)
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    epoch_loss = running_loss / total
    epoch_acc = correct / total
    return epoch_loss, epoch_acc, np.array(all_preds), np.array(all_labels)

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logging.info(f"Using device: {device}")
    
    # Import data loaders
    try:
        from utils.data_loaders import get_data_loaders
    except ImportError as e:
        logging.error(f"Could not import data loaders: {e}")
        sys.exit(1)
    
    # Load data
    data_dir = "data/PlantVillage/train"
    train_loader, val_loader, test_loader, class_names = get_data_loaders(
        data_dir,
        train_ratio=0.70,
        val_ratio=0.15,
        test_ratio=0.15,
        batch_size=32,
        num_workers=4 if torch.cuda.is_available() else 0
    )
    
    num_classes = len(class_names)
    logging.info(f"Number of classes: {num_classes}")
    logging.info(f"Class names: {class_names}")
    
    # Build model
    model = build_model(num_classes=num_classes, freeze_backbone=True)
    model = model.to(device)
    
    # Load checkpoint
    checkpoint_path = "saved_models/plantvillage_run/best_head_model.pth"
    if not os.path.exists(checkpoint_path):
        logging.error(f"Checkpoint not found: {checkpoint_path}")
        sys.exit(1)
    
    logging.info(f"Loading checkpoint: {checkpoint_path}")
    checkpoint = torch.load(checkpoint_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    
    criterion = nn.CrossEntropyLoss()
    
    # Evaluate on test set
    logging.info("="*60)
    logging.info("FINAL TEST SET EVALUATION")
    logging.info("="*60)
    
    test_loss, test_acc, test_preds, test_labels = evaluate(model, test_loader, criterion, device)
    precision, recall, f1, _ = precision_recall_fscore_support(test_labels, test_preds, average='macro')
    
    logging.info(f"Test Loss: {test_loss:.4f}")
    logging.info(f"Test Accuracy:  {test_acc*100:.2f}%")
    logging.info(f"Test Precision: {precision*100:.2f}%")
    logging.info(f"Test Recall:    {recall*100:.2f}%")
    logging.info(f"Test F1 Score:  {f1*100:.2f}%")
    
    # Validation metrics too
    val_loss, val_acc, val_preds, val_labels = evaluate(model, val_loader, criterion, device)
    val_precision, val_recall, val_f1, _ = precision_recall_fscore_support(val_labels, val_preds, average='macro')
    
    logging.info("="*60)
    logging.info("VALIDATION SET METRICS")
    logging.info("="*60)
    logging.info(f"Val Loss: {val_loss:.4f}")
    logging.info(f"Val Accuracy:  {val_acc*100:.2f}%")
    logging.info(f"Val Precision: {val_precision*100:.2f}%")
    logging.info(f"Val Recall:    {val_recall*100:.2f}%")
    logging.info(f"Val F1 Score:  {val_f1*100:.2f}%")
    
    # Save metrics
    metrics = {
        'checkpoint': checkpoint_path,
        'device': str(device),
        'num_classes': num_classes,
        'class_names': class_names,
        'test_metrics': {
            'loss': float(test_loss),
            'accuracy': float(test_acc),
            'precision': float(precision),
            'recall': float(recall),
            'f1': float(f1)
        },
        'validation_metrics': {
            'loss': float(val_loss),
            'accuracy': float(val_acc),
            'precision': float(val_precision),
            'recall': float(val_recall),
            'f1': float(val_f1)
        }
    }
    
    metrics_path = "saved_models/plantvillage_run/final_metrics.json"
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    logging.info(f"Metrics saved to: {metrics_path}")
    
    # Export to ONNX
    logging.info("="*60)
    logging.info("EXPORTING TO ONNX")
    logging.info("="*60)
    
    # Unfreeeze model for ONNX export
    model = model.cpu()
    model.eval()
    
    # Create dummy input
    dummy_input = torch.randn(1, 3, 224, 224)
    
    onnx_path = "saved_models/model.onnx"
    os.makedirs(os.path.dirname(onnx_path), exist_ok=True)
    
    try:
        torch.onnx.export(
            model,
            dummy_input,
            onnx_path,
            input_names=['input'],
            output_names=['output'],
            dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}},
            opset_version=14,
            do_constant_folding=True,
            verbose=False
        )
        logging.info(f"Model exported to: {onnx_path}")
    except Exception as e:
        logging.error(f"Failed to export ONNX model: {e}")
        sys.exit(1)
    
    # Validate ONNX
    logging.info("Validating ONNX model...")
    try:
        import onnx
        onnx_model = onnx.load(onnx_path)
        onnx.checker.check_model(onnx_model)
        logging.info("ONNX model validation successful!")
    except ImportError:
        logging.warning("ONNX not installed; skipping structural validation")
    except Exception as e:
        logging.error(f"ONNX validation failed: {e}")
    
    # Test ONNX inference
    logging.info("Testing ONNX inference...")
    try:
        import onnxruntime as ort
        
        session = ort.InferenceSession(onnx_path)
        input_name = session.get_inputs()[0].name
        output_name = session.get_outputs()[0].name
        
        # Compare on a batch from test set
        model = model.to(device)
        matched = 0
        total = 0
        
        with torch.no_grad():
            for images, labels in test_loader:
                images_np = images.numpy().astype(np.float32)
                
                # PyTorch prediction
                torch_outputs = model(images.to(device))
                torch_preds = torch.argmax(torch_outputs, dim=1).cpu().numpy()
                
                # ONNX prediction
                onnx_outputs = session.run([output_name], {input_name: images_np})
                onnx_preds = np.argmax(onnx_outputs[0], axis=1)
                
                matched += np.sum(torch_preds == onnx_preds)
                total += len(torch_preds)
                
                if total >= 320:  # Test on 10 batches
                    break
        
        match_rate = matched / total * 100
        logging.info(f"PyTorch vs ONNX match rate: {match_rate:.2f}%")
        
        if match_rate > 99.0:
            logging.info("ONNX inference validation successful!")
        else:
            logging.warning(f"ONNX inference match rate is only {match_rate:.2f}%")
            
    except ImportError:
        logging.warning("onnxruntime not installed; skipping inference validation")
    except Exception as e:
        logging.error(f"ONNX inference validation failed: {e}")
    
    logging.info("="*60)
    logging.info("Evaluation and export complete!")
    logging.info("="*60)

if __name__ == "__main__":
    main()
