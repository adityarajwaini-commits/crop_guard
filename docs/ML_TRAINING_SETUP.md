# CropGuard ML Training Setup

## Overview

This document describes the complete training pipeline for CropGuard, a ResNet-50 based plant disease classification model trained on the PlantVillage dataset.

## Project Structure

```
plant_ai/
├── training_colab.ipynb           # Complete Google Colab notebook
├── train_full_pipeline.py         # Standalone training script
├── training_requirements.txt      # GPU training dependencies
├── TRAINING_GUIDE.md              # Detailed training guide
├── config.py                      # Configuration (image size, batch size, etc.)
├── evaluate.py                    # Evaluation script
├── export_onnx.py                 # ONNX export script
├── onnx_predict.py                # ONNX inference wrapper
├── models/
│   ├── train.py                   # Training pipeline (build_model, train_one_epoch, etc.)
│   ├── predict.py                 # PyTorch predictor
│   ├── utils.py                   # EarlyStopping, etc.
│   └── __init__.py
├── utils/
│   ├── data_loaders.py            # ImageFolder loaders with train/val/test split
│   ├── dataset.py                 # PlantVillageDataset class
│   ├── transforms.py              # Data augmentations
│   └── __init__.py
├── saved_models/                  # Output directory for checkpoints
│   ├── best_head_model.pth        # Best checkpoint from Phase 1
│   ├── best_model.pth             # Best checkpoint from Phase 2 (FINAL)
│   ├── model.onnx                 # ONNX exported model
│   ├── class_names.txt            # List of all classes
│   ├── training_curves.png        # Loss & accuracy curves
│   ├── confusion_matrix.png       # Test set confusion matrix
│   └── training_report.json       # Training history
└── data/
    └── PlantVillage/              # Dataset root (must download)
        ├── Apple___Apple_scab/
        ├── Tomato___Early_blight/
        └── ... (38 total classes)
```

## Quick Start

### For Google Colab (Recommended)

1. **Upload project to Google Drive:**
   ```bash
   # Compress and upload plant_ai to your Google Drive
   zip -r plant_ai.zip plant_ai/
   ```

2. **Open notebook in Colab:**
   - Go to https://colab.research.google.com
   - Click "Upload" and select `training_colab.ipynb`
   - Or: right-click the notebook in Google Drive → "Open with" → "Google Colaboratory"

3. **Set runtime to GPU:**
   - Runtime → Change runtime type → GPU (T4 or better)

4. **Execute all cells in order:**
   - Cells 1-3: Setup and dependencies
   - Cells 4-5: Download and verify dataset
   - Cells 6-13: Training pipeline
   - Cells 14-21: Evaluation, ONNX export, download results

### For Local GPU Machine

```bash
# 1. Create environment
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

# 2. Install dependencies
pip install -r training_requirements.txt

# 3. Download PlantVillage dataset to data/PlantVillage/

# 4. Run training
python train_full_pipeline.py \
  --data_dir data/PlantVillage \
  --save_dir saved_models \
  --epochs 20 \
  --batch_size 32 \
  --learning_rate 0.001
```

### For Lambda Labs (or other GPU cloud)

Same as local GPU machine, but:
1. SSH into instance after launch
2. Clone repo: `git clone <repo-url>`
3. Follow "Local GPU Machine" steps above

## Dataset

### Download

**Option 1: Kaggle (Recommended)**
```bash
kaggle datasets download -d jbuchheim/plantvillage
unzip plantvillage.zip -d data/
```

**Option 2: Mendeley Data**
- Visit: https://data.mendeley.com/datasets/tywbtsjrjv/1
- Download and extract to `data/PlantVillage/`

### Expected Structure

```
data/PlantVillage/
├── Apple___Apple_scab/               (1645 images)
├── Tomato___Early_blight/            (1000 images)
├── Tomato___Late_blight/             (1155 images)
├── Tomato___Septoria_leaf_spot/      (1771 images)
└── ... (34 more classes)

Total: ~54,000 images across 38 classes
Dataset size: ~2-3 GB
```

### Verify Download

```bash
# Count classes
find data/PlantVillage -mindepth 1 -maxdepth 1 -type d | wc -l

# Count total images
find data/PlantVillage -type f | wc -l

# Check size
du -sh data/PlantVillage
```

## Training Details

### Model Architecture

- **Backbone:** ResNet-50 (ImageNet pretrained)
- **Classification Head:** Custom head (2048 → 512 → num_classes)
- **Framework:** PyTorch
- **Loss:** CrossEntropyLoss
- **Optimizer:** Adam

### Training Strategy (Two-Phase)

**Phase 1: Head Training (10-15 epochs)**
- Backbone: **frozen**
- Learning rate: **0.001**
- Focus: Train classification head on ImageNet features
- Output: `best_head_model.pth`

**Phase 2: Fine-tuning (5-10 epochs)**
- Backbone: **unfrozen**
- Learning rate: **0.00001** (100x lower)
- Focus: Adapt backbone to plant diseases
- Output: `best_model.pth` (FINAL)

### Hyperparameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Batch Size | 32 | Adjust for GPU VRAM (16-64) |
| Learning Rate (Phase 1) | 0.001 | Adam optimizer |
| Learning Rate (Phase 2) | 0.00001 | 100x reduction |
| Scheduler | ReduceLROnPlateau | Reduce LR if no improvement |
| Early Stopping | Patience 5 | Stop if loss doesn't improve |
| Epochs (Phase 1) | 10-15 | Set via `--epochs` arg |
| Epochs (Phase 2) | 5-10 | Auto-calculated (50% of Phase 1) |
| Data Split | 70/15/15 | Train/Val/Test |

### Data Augmentation (Training)

```python
transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(degrees=30),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],  # ImageNet
        std=[0.229, 0.224, 0.225]
    )
])
```

### Validation/Test Transform (No Augmentation)

```python
transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])
```

## Expected Results

### Training Performance

| Hardware | Batch 32 | Time/Epoch | Total Time |
|----------|----------|-----------|-----------|
| RTX 3060 Ti | 2-3 min | 30-45 min | 10-15h |
| RTX 4090 | 1 min | 15-20 min | 5-8h |
| Tesla V100 | 1 min | 15-20 min | 5-8h |
| Colab T4 | 3-5 min | 60-100 min | 20-30h |
| CPU (not recommended) | — | hours | days |

### Model Accuracy

- **Test Accuracy:** 90-98% (class-dependent)
- **Precision:** 88-96% (macro-avg)
- **Recall:** 88-96% (macro-avg)
- **F1 Score:** 88-96% (macro-avg)

## Post-Training

### Step 1: Evaluate on Test Set

```bash
python evaluate.py \
  --model_path saved_models/best_model.pth \
  --data_dir data/PlantVillage
```

**Outputs:**
- `saved_models/evaluation_report.txt` (metrics)
- `saved_models/confusion_matrix.png` (visualization)

### Step 2: Export to ONNX

```bash
python export_onnx.py
```

**Outputs:**
- `saved_models/model.onnx` (ONNX format)
- `saved_models/class_names.txt` (class list)
- Validation and benchmark report printed to console

### Step 3: Integrate with Backend

1. Copy `saved_models/best_model.pth` and `saved_models/model.onnx` to local project

2. Update `backend/app/api/routes.py`:
   ```python
   # Replace mock with real ONNX predictor
   from onnx_predict import ONNXCropGuardPredictor
   
   predictor = ONNXCropGuardPredictor()
   prediction = predictor.predict(image, top_k=3)
   ```

3. Test end-to-end:
   ```bash
   # Terminal 1: Backend
   cd backend
   python -m uvicorn app.main:app --reload
   
   # Terminal 2: Frontend
   cd frontend
   npm run dev
   
   # Browser: http://localhost:5173
   # Upload test image → verify predictions
   ```

## Files Generated

After training completes, the following files will be in `saved_models/`:

- **best_head_model.pth** (Phase 1 checkpoint, ~100 MB)
- **best_model.pth** (Final checkpoint, ~100 MB) ← Use this for predictions
- **model.onnx** (ONNX export, ~100 MB)
- **class_names.txt** (38 disease classes, one per line)
- **training_report.json** (Training history with loss/accuracy per epoch)
- **training_curves.png** (Loss & accuracy plots)
- **confusion_matrix.png** (Test set confusion matrix)
- **evaluation_report.txt** (Per-class metrics)

## Troubleshooting

### Out of Memory (OOM)

```bash
# Reduce batch size
python train_full_pipeline.py --batch_size 16

# Or reduce image size in config.py
Config.IMAGE_SIZE = (192, 192)
```

### Slow Training on Colab

- Ensure GPU runtime is selected (not CPU)
- Increase batch size if memory allows
- Close other Colab tabs to free resources

### Dataset Not Found

```bash
# Verify dataset path
ls data/PlantVillage/
find data/PlantVillage -type f | wc -l  # Should show ~54,000
```

### CUDA Out of Memory

```bash
# In Python/Jupyter
torch.cuda.empty_cache()

# Restart kernel/session
# Reduce batch size or image size
```

## Performance Tips

1. **Increase Batch Size:** Speeds up training (if GPU memory allows)
2. **Use Higher Learning Rate:** Faster convergence (but may miss optimal)
3. **Reduce Image Size:** Faster (but may lose details)
4. **Use Mixed Precision:** Faster and less memory (requires `torch.cuda.amp`)
5. **Use Better GPU:** V100/A100 are 5-10x faster than T4

## Next Steps

1. Download PlantVillage dataset (~2-3 GB)
2. Choose training environment (Colab recommended)
3. Execute training notebook or script
4. Export to ONNX
5. Download `best_model.pth` and `model.onnx`
6. Copy to `saved_models/` in local project
7. Update backend to use ONNX model
8. Test with frontend
9. Deploy!

## References

- **PyTorch Transfer Learning:** https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html
- **PlantVillage Dataset:** https://data.mendeley.com/datasets/tywbtsjrjv/1
- **ONNX Runtime:** https://onnxruntime.ai/
- **Google Colab:** https://colab.research.google.com/

## Support

For issues:
1. Check `saved_models/training_report.json` for training history
2. Review `confusion_matrix.png` for misclassified classes
3. Verify dataset integrity (`data/PlantVillage/`)
4. Check GPU memory usage
5. Review validation accuracy trend (should monotonically increase)

---

**Last Updated:** 2024  
**Version:** 1.0.0  
**Status:** Ready for GPU training
