import os, json, traceback

print('cwd:', os.getcwd())
print('saved_models/model.onnx exists:', os.path.exists('saved_models/model.onnx'))
print('saved_models/plantvillage_run/final_metrics.json exists:', os.path.exists('saved_models/plantvillage_run/final_metrics.json'))

try:
    from models.onnx_predictor import ONNXPredictor
    p = ONNXPredictor()
    print('Loaded predictor OK')
    info = p.get_model_info()
    print('model_info keys:', list(info.keys()))
except Exception as e:
    traceback.print_exc()
    print('EXC_STR:', str(e))
