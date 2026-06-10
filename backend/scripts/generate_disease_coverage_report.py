"""
Generate a coverage report comparing the model class names (from final_metrics.json)
against entries in the backend disease database.

Saves report to: saved_models/plantvillage_run/disease_coverage_report.json
Prints a brief summary to stdout.
"""
import os
import json
from pathlib import Path

# Paths (project root assumed to be two levels up from this script)
ROOT = Path(__file__).resolve().parent.parent.parent
METRICS_PATH = ROOT / "saved_models" / "plantvillage_run" / "final_metrics.json"
REPORT_PATH = ROOT / "saved_models" / "plantvillage_run" / "disease_coverage_report.json"

# Import database lookup
import importlib.util

# Load disease_database module by file path (avoid package import issues)
DB_PATH = ROOT / "backend" / "app" / "models" / "disease_database.py"
spec = importlib.util.spec_from_file_location("disease_database", str(DB_PATH))
disease_db = importlib.util.module_from_spec(spec)
spec.loader.exec_module(disease_db)

DISEASE_DATABASE = disease_db.DISEASE_DATABASE
get_disease_info = disease_db.get_disease_info


def _normalize(name: str) -> str:
    if not name or not isinstance(name, str):
        return ''
    name = name.replace('___', ' ')
    name = name.replace('_', ' ')
    name = ' '.join(name.split())
    return name.strip().lower()


def main():
    if not METRICS_PATH.exists():
        print(f"Metrics file not found: {METRICS_PATH}")
        return 1

    data = json.loads(METRICS_PATH.read_text(encoding='utf-8'))
    class_names = data.get('class_names') or data.get('classes') or []

    total = len(class_names)
    classes_with_info = []
    classes_missing = []

    # Build normalized db keys
    normalized_db_keys = { _normalize(k): k for k in DISEASE_DATABASE.keys() }

    for cls in class_names:
        normalized = _normalize(cls)
        if normalized in normalized_db_keys:
            classes_with_info.append({
                'class': cls,
                'matched_db_key': normalized_db_keys[normalized]
            })
        else:
            # Try get_disease_info to see if normalization in function catches it
            info = get_disease_info(cls)
            # If info has real symptoms (not the default placeholder), consider it found
            if info.get('symptoms') and info.get('symptoms') != ["Unable to retrieve symptoms"]:
                classes_with_info.append({
                    'class': cls,
                    'matched_db_key': info.get('name', 'Unknown')
                })
            else:
                classes_missing.append(cls)

    report = {
        'total_classes': total,
        'classes_with_info_count': len(classes_with_info),
        'classes_missing_count': len(classes_missing),
        'classes_with_info': classes_with_info,
        'classes_missing': classes_missing
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding='utf-8')

    print(f"Total classes: {total}")
    print(f"Classes with disease information: {len(classes_with_info)}")
    print(f"Classes missing disease information: {len(classes_missing)}")
    print(f"Saved report to: {REPORT_PATH}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
