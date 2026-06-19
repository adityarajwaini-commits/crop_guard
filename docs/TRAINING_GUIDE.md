# CropGuard: Complete Training Guide

## Overview

This guide covers training the CropGuard ResNet-50 model on the PlantVillage dataset. Since the local development machine lacks CUDA GPU support, training will be performed on a GPU environment such as Google Colab, Lambda Labs, or a cloud GPU instance.

## Dataset Setup

### Step 1: Download PlantVillage Dataset

The PlantVillage dataset contains ~54,000 labeled leaf images across ~38 disease classes and healthy plant samples.

**Option A: Kaggle (Recommended)**

1. Create a Kaggle account: https://www.kaggle.com
2. Download Kaggle API credentials: https://www.kaggle.com/settings/account
3. Install Kaggle CLI:
   ```bash
   pip install kaggle
   ```
4. Place your `kaggle.json` in `~/.kaggle/` (or `%USERPROFILE%\.kaggle\` on Windows)
5. Download and extract:
   ```bash
   kaggle datasets download -d jbuchheim/plantvillage
   unzip plantvillage.zip -d data/
   ```

**Option B: Direct Download**

Visit https://data.mendeley.com/datasets/tywbtsjrjv/1 and manually download the dataset to `data/PlantVillage/`

**Option C: Google Drive (for Colab)**

1. Upload the dataset ZIP to your Google Drive
2. In Colab, mount Drive and extract:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   
   !unzip /content/drive/MyDrive/plantvillage.zip -d /content/data/
   ```

### Step 2: Verify Dataset Structure

Expected folder structure:
```
data/
├── PlantVillage/
│   ├── Apple___Apple_scab/
│   │   ├── img001.jpg
│   │   ├── img002.jpg
│   │   └── ...
│   ├── Tomato___Early_blight/
│   ├── Tomato___Late_blight/
│   └── ... (38 total classes)
```

Quick verification:
```bash
# Count classes
find data/PlantVillage -mindepth 1 -maxdepth 1 -type d | wc -l

# Count total images
find data/PlantVillage -type f | wc -l

# Check dataset size
du -sh data/PlantVillage
```

## Training Environment Setup

### Option 1: Google Colab (Recommended for Beginners)

1. Open Google Colab: https://colab.research.google.com
2. Create a new notebook
3. Run the cells in `training_colab.ipynb` (see Colab Notebook section)

**Colab GPU Settings:**
- Runtime → Change runtime type → GPU (Tesla K80, V100, or T4)

### Option 2: Local GPU Machine

**Requirements:**
- NVIDIA GPU with 8GB+ VRAM (RTX 3060, RTX 4070, A100, etc.)
- CUDA Toolkit 11.8+
- cuDNN 8.0+

**Installation:**
```bash
# 1. Create virtual environment
python -m venv cropguard_env
source cropguard_env/bin/activate  # On Windows: cropguard_env\Scripts\activate

# 2. Install PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 3. Install project dependencies
pip install -r training_requirements.txt

# 4. Copy dataset to data/PlantVillage/
cp -r /path/to/plantvillage data/
```

### Option 3: Lambda Labs GPU Cloud

1. Create account: https://www.lambdalabs.com/
2. Launch GPU instance (Ubuntu 20.04 + NVIDIA GPU)
3. SSH into instance
4. Follow Option 2 setup steps
5. Clone repository and download dataset

## Training Workflow

### Local GPU or Lambda Labs

```bash
# From project root
python train_full_pipeline.py \
  --data_dir data/PlantVillage \
  --save_dir saved_models \
  --epochs 20 \
  --batch_size 32 \
  --learning_rate 0.001
```

**Expected output:**
- `saved_models/best_head_model.pth` (head-only training checkpoint)
- `saved_models/best_model.pth` (fine-tuned full model)
- `saved_models/training_report.json` (training history)

### Google Colab

Use `training_colab.ipynb` notebook with integrated cells for:
- Dataset download
- Environment setup
- Model training
- ONNX export
- Results visualization

## Training Pipeline Details

### Architecture

- **Backbone:** ResNet-50 (ImageNet pretrained)
- **Head:** Custom classification layer (fc: 2048→512→num_classes)
- **Framework:** PyTorch

### Training Phases

**Phase 1: Classification Head Training (10-15 epochs)**
- Backbone frozen; only head trained
- Higher learning rate (0.001)
- Faster convergence
- Checkpoint: `best_head_model.pth`

**Phase 2: Fine-tuning (5-10 epochs)**
- Full network unfrozen
- Reduced learning rate (0.00001)
- Improves backbone features
- Checkpoint: `best_model.pth` (final)

### Hyperparameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Batch Size | 32 | Adjust for GPU VRAM (16-64) |
| Learning Rate (Phase 1) | 0.001 | Adam optimizer |
| Learning Rate (Phase 2) | 0.00001 | 100x reduction |
| Optimizer | Adam | Adaptive learning rate |
| Scheduler | ReduceLROnPlateau | Reduce LR if loss plateaus |
| Early Stopping | Patience 5 | Stop if no improvement after 5 epochs |
| Data Split | 70/15/15 | Train/Val/Test |
| Epochs | 20 | Phase 1: 10-15, Phase 2: 5-10 |

### Data Augmentation (Train Set)

- Random resize and crop
- Random horizontal flip (p=0.5)
- Random rotation (±30°)
- Color jitter (brightness, contrast, saturation)
- Normalization (ImageNet mean/std)

### Validation & Test Transforms

- Resize to 224×224
- CenterCrop
- Normalization (ImageNet mean/std)

## Expected Training Time & Results

### GPU Performance Estimates

| GPU | Batch 32 | Time per Epoch | Total Time (20 epochs) |
|-----|----------|----------------|----------------------|
| RTX 3060 Ti | ~2-3 min | 40-60 min | ~15-20 hours |
| RTX 4090 | ~1 min | 15-20 min | ~5-8 hours |
| Tesla V100 | ~1 min | 15-20 min | ~5-8 hours |
| Google Colab T4 | ~3-5 min | 60-100 min | ~20-30 hours |

### Expected Accuracy

- **Accuracy:** 90-98% (depends on class difficulty)
- **Precision:** 88-96% (macro-average)
- **Recall:** 88-96% (macro-average)
- **F1 Score:** 88-96% (macro-average)

## Post-Training Steps

### Step 1: Evaluate on Test Set

```bash
python evaluate.py \
  --model_path saved_models/best_model.pth \
  --data_dir data/PlantVillage
```

**Output:**
- `saved_models/evaluation_report.txt` (metrics summary)
- `saved_models/confusion_matrix.png` (visualization)

### Step 2: Export to ONNX

```bash
python export_onnx.py
```

**Output:**
- `saved_models/model.onnx` (ONNX runtime model)
- `saved_models/class_names.txt` (class list)
- Validation report and latency benchmark

### Step 3: Copy to Project

Copy trained files back to local development machine:
```bash
# From GPU machine
scp -r saved_models/ user@dev-machine:/path/to/plant_ai/

# Or from Colab: Download files
# Click Files → Right-click saved_models → Download
```

## Backend Integration

Once trained model and ONNX files are in `saved_models/`:

1. **Update backend/app/api/routes.py** to use real ONNX predictor:
   ```python
   # Replace mock with real ONNX inference
   from onnx_predict import ONNXCropGuardPredictor
   predictor = ONNXCropGuardPredictor()
   prediction = predictor.predict(image_pil, top_k=3)
   ```

2. **Remove mock fallback** in `/api/predict` endpoint

3. **Test end-to-end:**
   - Start backend: `uvicorn app.main:app --reload`
   - Start frontend: `npm run dev`
   - Upload test image → verify predictions

## Troubleshooting

### Out of Memory (OOM)

- Reduce batch size: `--batch_size 16` or `--batch_size 8`
- Reduce image size: modify `Config.IMAGE_SIZE` to `(192, 192)`

### Slow Training on Colab

- Use GPU runtime (not CPU)
- Reduce dataset size (sample classes)
- Increase batch size if memory allows

### Dataset Not Found

- Verify path: `data/PlantVillage/` exists
- Check folder structure matches expected format
- Run verification commands (see Dataset Setup)

### CUDA Out of Memory

- Restart Colab runtime
- Clear cache: `torch.cuda.empty_cache()`
- Reduce batch size

## Checkpointing & Resume

If training is interrupted:

1. Resume from last checkpoint:
   ```bash
   # Modify train_full_pipeline.py to load checkpoint before training
   checkpoint = torch.load(save_dir + "/best_model.pth")
   model.load_state_dict(checkpoint['model_state_dict'])
   ```

2. Or start fresh with same hyperparameters

## Next Steps

1. Download and verify PlantVillage dataset
2. Choose training environment (Colab recommended)
3. Run training pipeline
4. Export to ONNX
5. Copy `best_model.pth` and `model.onnx` to `saved_models/`
6. Integrate with backend
7. Deploy!

## Additional Resources

- PyTorch Transfer Learning Tutorial: https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html
- PlantVillage Dataset: https://data.mendeley.com/datasets/tywbtsjrjv/1
- ONNX Runtime: https://onnxruntime.ai/
- Google Colab: https://colab.research.google.com/

## Support

For issues or questions:
1. Check logs in `training_report.json`
2. Review confusion matrix for misclassified classes
3. Verify dataset integrity
4. Check GPU memory usage
5. Review validation accuracy trends

---

**Last Updated:** 2024
**Version:** 1.0.0
