import os, sys, traceback

# Simulate running from backend/ as uvicorn was started there
os.chdir('backend')
# Add project root to path (same logic as routes.py)
PROJECT_ROOT = os.path.dirname(os.getcwd())
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

print('cwd:', os.getcwd())
print('sys.path[0]:', sys.path[0])

try:
    from models.onnx_predictor import ONNXPredictor
    p = ONNXPredictor()
    print('Loaded predictor OK')
    print('model path:', p.model_path)
except Exception as e:
    traceback.print_exc()
    print('EXC_STR:', str(e))
