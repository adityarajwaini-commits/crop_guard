#!/usr/bin/env python3
"""
GPU Verification Script for CropGuard AI Training
Checks CUDA availability, GPU detection, and basic GPU operations
"""

import sys
import torch
import subprocess

def print_section(title):
    """Print formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def main():
    print_section("PYTORCH & GPU VERIFICATION")
    
    # 1. PyTorch Version
    print(f"\n1. PyTorch Version:")
    print(f"   Version: {torch.__version__}")
    
    # 2. CUDA Availability
    print(f"\n2. CUDA Availability:")
    print(f"   CUDA Available: {torch.cuda.is_available()}")
    
    if not torch.cuda.is_available():
        print("\n❌ ERROR: CUDA is not available!")
        print("   PyTorch may have been installed for CPU only.")
        return False
    
    print(f"   ✅ CUDA is available!")
    
    # 3. CUDA Version
    print(f"\n3. CUDA Version:")
    print(f"   CUDA Version: {torch.version.cuda}")
    print(f"   cuDNN Version: {torch.backends.cudnn.version()}")
    
    # 4. GPU Detection
    print(f"\n4. GPU Information:")
    num_gpus = torch.cuda.device_count()
    print(f"   Number of GPUs: {num_gpus}")
    
    if num_gpus == 0:
        print("❌ ERROR: No GPUs detected!")
        return False
    
    for i in range(num_gpus):
        print(f"\n   GPU {i}:")
        print(f"     Name: {torch.cuda.get_device_name(i)}")
        props = torch.cuda.get_device_properties(i)
        print(f"     Compute Capability: {props.major}.{props.minor}")
        print(f"     Total Memory: {props.total_memory / (1024**3):.2f} GB")
    
    print(f"\n   Current Device: {torch.cuda.current_device()}")
    print(f"   Current Device Name: {torch.cuda.get_device_name()}")
    
    # 5. Memory Status
    print(f"\n5. GPU Memory Status:")
    print(f"   Allocated: {torch.cuda.memory_allocated() / (1024**3):.2f} GB")
    print(f"   Reserved: {torch.cuda.memory_reserved() / (1024**3):.2f} GB")
    print(f"   Available: {(torch.cuda.get_device_properties(0).total_memory - torch.cuda.memory_reserved()) / (1024**3):.2f} GB")
    
    # 6. Basic GPU Operations Test
    print(f"\n6. GPU Tensor Operations Test:")
    try:
        # Create tensors on GPU
        x = torch.randn(1000, 1000, device='cuda')
        y = torch.randn(1000, 1000, device='cuda')
        
        # Perform computation
        import time
        start = time.time()
        z = torch.mm(x, y)
        torch.cuda.synchronize()
        gpu_time = time.time() - start
        
        print(f"   ✅ GPU tensor operations successful!")
        print(f"   Matrix multiplication time (GPU): {gpu_time*1000:.2f} ms")
        
        # CPU comparison
        x_cpu = x.cpu()
        y_cpu = y.cpu()
        start = time.time()
        z_cpu = torch.mm(x_cpu, y_cpu)
        cpu_time = time.time() - start
        
        print(f"   Matrix multiplication time (CPU): {cpu_time*1000:.2f} ms")
        print(f"   Speedup: {cpu_time/gpu_time:.2f}x")
        
    except Exception as e:
        print(f"   ❌ GPU operations failed: {e}")
        return False
    
    # 7. nvidia-smi Check
    print(f"\n7. System GPU Status (nvidia-smi):")
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            # Print first 15 lines which contain the GPU info
            for line in lines[:15]:
                if line.strip():
                    print(f"   {line}")
        else:
            print("   ⚠ Could not run nvidia-smi")
    except Exception as e:
        print(f"   ⚠ nvidia-smi error: {e}")
    
    # Final Summary
    print_section("VERIFICATION SUMMARY")
    print(f"\n✅ GPU VERIFICATION PASSED!")
    print(f"\nYour GPU Setup:")
    print(f"  • PyTorch: {torch.__version__}")
    print(f"  • GPU: {torch.cuda.get_device_name()}")
    print(f"  • CUDA: {torch.version.cuda}")
    print(f"  • Memory: {torch.cuda.get_device_properties(0).total_memory / (1024**3):.2f} GB")
    print(f"\n✅ Ready for training!")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
