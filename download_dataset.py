#!/usr/bin/env python3
"""
PlantVillage Dataset Download & Verification Script
Supports multiple download methods: Kaggle API, manual download, or alternative sources
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_section(title):
    """Print formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def check_kaggle_api():
    """Check if Kaggle API is installed and configured"""
    try:
        import kaggle
        print("✅ Kaggle API installed")
        
        # Check for credentials
        kaggle_dir = Path.home() / '.kaggle'
        json_file = kaggle_dir / 'kaggle.json'
        
        if json_file.exists():
            print("✅ Kaggle credentials found")
            return True
        else:
            print("⚠ Kaggle credentials not found")
            print(f"  Download from: https://www.kaggle.com/settings/account")
            print(f"  Save to: {json_file}")
            return False
    except ImportError:
        print("⚠ Kaggle API not installed")
        print("  Install with: pip install kaggle")
        return False

def download_with_kaggle():
    """Download PlantVillage dataset using Kaggle API"""
    dataset_id = "jbuchheim/plantvillage"
    output_dir = Path("data/plantvillage_raw")
    
    print(f"Downloading {dataset_id}...")
    print(f"Output directory: {output_dir}")
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        subprocess.run([
            'kaggle', 'datasets', 'download', 
            '-d', dataset_id,
            '-p', str(output_dir),
            '--unzip'
        ], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Download failed: {e}")
        return False

def verify_dataset(data_dir="data/plantvillage_raw"):
    """Verify downloaded dataset structure and contents"""
    print_section("VERIFYING DATASET")
    
    data_path = Path(data_dir)
    
    if not data_path.exists():
        print(f"❌ Dataset directory not found: {data_path}")
        return False
    
    print(f"✅ Dataset directory found: {data_path}")
    
    # Count files
    image_files = list(data_path.rglob('*.jpg')) + list(data_path.rglob('*.JPG')) + \
                  list(data_path.rglob('*.png')) + list(data_path.rglob('*.PNG'))
    
    print(f"\n📊 Dataset Statistics:")
    print(f"   Total image files: {len(image_files)}")
    
    # Count by subdirectory (disease classes)
    classes = {}
    for img_file in image_files:
        class_name = img_file.parent.name
        classes[class_name] = classes.get(class_name, 0) + 1
    
    print(f"   Number of disease classes: {len(classes)}")
    print(f"\n   Classes found:")
    for class_name in sorted(classes.keys()):
        print(f"      {class_name}: {classes[class_name]} images")
    
    # Calculate size
    total_size_gb = sum(f.stat().st_size for f in image_files) / (1024**3)
    print(f"\n   Total dataset size: {total_size_gb:.2f} GB")
    
    # Validation checks
    issues = []
    
    if len(image_files) < 50000:
        issues.append(f"⚠ Expected ~54,000 images, found {len(image_files)}")
    
    if len(classes) < 38:
        issues.append(f"⚠ Expected ~38 disease classes, found {len(classes)}")
    
    if not issues:
        print(f"\n✅ Dataset verification PASSED!")
        return True
    else:
        print(f"\n⚠ Dataset verification issues:")
        for issue in issues:
            print(f"  {issue}")
        return len(image_files) > 1000  # Pass if we have enough data to start

def organize_dataset(raw_dir="data/plantvillage_raw", output_dir="data/PlantVillage"):
    """Organize dataset for training (optional preprocessing)"""
    print_section("ORGANIZING DATASET")
    
    raw_path = Path(raw_dir)
    output_path = Path(output_dir)
    
    if not raw_path.exists():
        print(f"❌ Raw dataset not found: {raw_path}")
        return False
    
    # Create output directory
    os.makedirs(output_path, exist_ok=True)
    
    print(f"Organizing dataset from {raw_path} to {output_path}...")
    
    # Symlink or copy subdirectories
    for class_dir in raw_path.iterdir():
        if class_dir.is_dir():
            output_class_dir = output_path / class_dir.name
            
            if not output_class_dir.exists():
                try:
                    # Try symlink first (faster)
                    os.symlink(class_dir, output_class_dir)
                    print(f"  ✅ Linked: {class_dir.name}")
                except (OSError, NotImplementedError):
                    # Fallback to copying
                    import shutil
                    shutil.copytree(class_dir, output_class_dir)
                    print(f"  ✅ Copied: {class_dir.name}")
    
    return True

def main():
    print_section("PLANTVILLAGE DATASET SETUP")
    
    # Check current status
    dataset_paths = [Path("data/PlantVillage"), Path("data/plantvillage_raw")]
    existing = [p for p in dataset_paths if p.exists()]
    
    if existing:
        print(f"✅ Dataset already exists at:")
        for path in existing:
            print(f"   {path}")
        
        print("\nVerifying existing dataset...")
        if verify_dataset(existing[0]):
            print("\n✅ Ready to train!")
            return True
    
    # Download options
    print("\n📥 Download Options:")
    print("\n1. Automatic (Kaggle API):")
    kaggle_available = check_kaggle_api()
    
    print("\n2. Manual Download:")
    print("   • Download from: https://www.kaggle.com/datasets/jbuchheim/plantvillage")
    print("   • Extract to: data/plantvillage_raw/")
    
    print("\n3. Alternative Sources:")
    print("   • Mendeley Data: https://data.mendeley.com/datasets/tywbtspgx9")
    print("   • Google Drive: Check CropGuard documentation")
    
    if kaggle_available:
        print("\n🚀 Ready to download with Kaggle API!")
        print("\nTo start download, run:")
        print("  python download_dataset.py --download")
    else:
        print("\n⚠ For Kaggle API download, first:")
        print("  1. pip install kaggle")
        print("  2. Download kaggle.json from https://www.kaggle.com/settings/account")
        print("  3. Place in ~/.kaggle/")
        print("  4. chmod 600 ~/.kaggle/kaggle.json  (Linux/Mac)")
    
    print("\nAfter dataset download:")
    print("  python download_dataset.py --verify")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='PlantVillage Dataset Manager')
    parser.add_argument('--download', action='store_true', help='Download dataset using Kaggle API')
    parser.add_argument('--verify', action='store_true', help='Verify existing dataset')
    parser.add_argument('--organize', action='store_true', help='Organize raw dataset for training')
    
    args = parser.parse_args()
    
    if args.download:
        if check_kaggle_api():
            if download_with_kaggle():
                verify_dataset()
        else:
            print("❌ Kaggle API not available. Please configure or download manually.")
    
    elif args.verify:
        verify_dataset()
    
    elif args.organize:
        organize_dataset()
    
    else:
        main()
