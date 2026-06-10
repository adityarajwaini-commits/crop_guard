from models.onnx_predictor import ONNXPredictor
import json

# Select three real images
images = [
    'data/PlantVillage/valid/Apple___healthy/14896dc0-688d-456f-b5ec-a037695b0193___RS_HL 6268.JPG',
    'data/PlantVillage/valid/Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot/0e0ed08d-3021-49a7-9098-7c90afeb2fd5___RS_GLSp 4346.JPG',
    'data/PlantVillage/train/Tomato___Late_blight/01425d17-4c97-46e3-b395-c1453b78ab78___GHLB2 Leaf 9100.JPG'
]

predictor = ONNXPredictor()
results = {}
for p in images:
    try:
        res = predictor.predict_path(p, top_k=3)
        results[p] = res
    except Exception as e:
        results[p] = {'error': str(e)}

print(json.dumps(results, indent=2))
