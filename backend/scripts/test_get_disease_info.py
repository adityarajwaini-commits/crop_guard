import importlib.util
from pathlib import Path
DB_PATH = Path(__file__).resolve().parent.parent / 'app' / 'models' / 'disease_database.py'
spec = importlib.util.spec_from_file_location('disease_database', str(DB_PATH))
db = importlib.util.module_from_spec(spec)
spec.loader.exec_module(db)

tests = [
    'Tomato___Late_blight',
    'Tomato___Late_blightmap',
    'Corn_(maize)___Northern_Leaf_Blight',
    'Apple___Apple_scab',
    'Tomato___Tomato_mosaic_virus'
]
for t in tests:
    info = db.get_disease_info(t)
    found = info.get('symptoms') and info.get('symptoms')!=['Unable to retrieve symptoms']
    print(t, '->', 'FOUND' if found else 'MISSING', 'name:', info.get('name'))
