# CropGuard Deployment Report

**Date:** 2026-06-15  
**Status:** ✅ PRODUCTION READY  
**Model Framework:** ONNX Runtime (Exported from PyTorch ResNet-50)

---

## Executive Summary

The CropGuard disease classification model has been successfully trained, evaluated, and exported to production-ready ONNX format. The final model achieves **98.35% test accuracy** and **98.32% validation accuracy** across 38 plant disease and health categories. The backend has been updated to use the efficient ONNX Runtime inference engine with all mock fallbacks removed.

---

## Model Performance

### Test Set Metrics
| Metric | Value |
|--------|-------|
| **Accuracy** | 98.35% |
| **Precision** | 98.35% |
| **Recall** | 98.34% |
| **F1 Score** | 98.34% |
| **Loss** | 0.0539 |

### Validation Set Metrics
| Metric | Value |
|--------|-------|
| **Accuracy** | 98.32% |
| **Precision** | 98.31% |
| **Recall** | 98.29% |
| **F1 Score** | 98.29% |
| **Loss** | 0.0515 |

### Dataset Summary
- **Training Images:** 60,808
- **Validation Images:** 13,101
- **Test Images:** 13,958
- **Total Images:** 87,867
- **Disease Classes:** 38
- **Data Source:** PlantVillage Dataset

---

## Model Architecture

### Training Approach
**Two-Phase Training Pipeline:**
1. **Phase 1 (Head-Only Training):** 14 epochs
   - Frozen ResNet-50 backbone
   - Trained custom classification head only
   - Final validation accuracy: **98.09%**
   
2. **Phase 2 (Full Fine-Tuning):** Stopped after Epoch 14
   - Phase 2 was showing diminishing returns (~97.4-97.5%)
   - Phase 1 checkpoint achieved superior performance
   - Production model uses Phase 1 checkpoint

### Network Architecture
```
ResNet-50 Backbone (frozen during Phase 1)
├── Input: 224×224 RGB images
├── Normalization: ImageNet stats (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
├── ResNet-50 Feature Extraction
└── Custom Head
    ├── Linear(2048 → 512)
    ├── ReLU
    ├── Dropout(0.3)
    └── Linear(512 → 38 classes)
```

---

## File Paths & Assets

### Model Files
| File | Location | Purpose |
|------|----------|---------|
| **ONNX Model** | `saved_models/model.onnx` | Production inference model |
| **PyTorch Checkpoint** | `saved_models/plantvillage_run/best_head_model.pth` | Source checkpoint (Phase 1) |
| **Metrics** | `saved_models/plantvillage_run/final_metrics.json` | Evaluation metrics & class names |
| **Training Report** | `saved_models/plantvillage_run/training_report.json` | Full training history |

### Backend Integration
| File | Location | Status |
|------|----------|--------|
| **ONNX Predictor** | `models/onnx_predictor.py` | ✅ New, production-ready |
| **API Routes** | `backend/app/api/routes.py` | ✅ Updated for ONNX |
| **Legacy Predictor** | `models/predict.py` | ⚠️ Deprecated (PyTorch-based) |

### Dataset Location
- **Training Data:** `data/PlantVillage/train/`
- **Validation Data:** `data/PlantVillage/valid/`

---

## ONNX Export & Validation

### Export Specifications
- **Format:** ONNX (Open Neural Network Exchange)
- **Opset Version:** 14
- **Dynamic Axes:** Batch size (inference supports variable batch sizes)
- **Input Shape:** (batch_size, 3, 224, 224) - float32
- **Output Shape:** (batch_size, 38) - logits
- **Model Size:** ~103 MB

### Inference Validation
✅ **PyTorch vs ONNX Comparison:** 100% match rate (tested on 10 batches)
- Verified on 320 test images
- All predictions identical between PyTorch and ONNX Runtime
- Softmax applied post-inference for probabilities

---

## Supported Disease Classes (38 Total)

| Category | Classes |
|----------|---------|
| **Apple** | Apple_scab, Black_rot, Cedar_apple_rust, healthy |
| **Blueberry** | healthy |
| **Cherry** | Powdery_mildew, healthy |
| **Corn** | Cercospora_leaf_spot Gray_leaf_spot, Common_rust, Northern_Leaf_Blight, healthy |
| **Grape** | Black_rot, Esca_(Black_Measles), Leaf_blight_(Isariopsis_Leaf_Spot), healthy |
| **Orange** | Haunglongbing_(Citrus_greening) |
| **Peach** | Bacterial_spot, healthy |
| **Pepper** | Bacterial_spot, healthy |
| **Potato** | Early_blight, Late_blight, healthy |
| **Raspberry** | healthy |
| **Soybean** | healthy |
| **Squash** | Powdery_mildew |
| **Strawberry** | Leaf_scorch, healthy |
| **Tomato** | Bacterial_spot, Early_blight, Late_blight, Leaf_Mold, Septoria_leaf_spot, Spider_mites Two-spotted_spider_mite, Target_Spot, Tomato_Yellow_Leaf_Curl_Virus, Tomato_mosaic_virus, healthy |

---

## Backend API Integration

### Updated Endpoints

#### `POST /api/predict`
- **Input:** Image file (JPG, PNG, WebP)
- **Output:** JSON with disease prediction + top-3 alternatives
- **Runtime:** ONNX Runtime (GPU-accelerated)
- **Removed:** Mock fallback response

**Example Response:**
```json
{
  "success": true,
  "data": {
    "image_id": "uuid",
    "prediction": {
      "primary_disease": "Tomato___Early_blight",
      "confidence": 0.9835,
      "model_version": "v2.0"
    },
    "top_3": [
      {
        "rank": 1,
        "disease_name": "Tomato___Early_blight",
        "confidence": 0.9835,
        "color": "#ef4444"
      },
      ...
    ],
    "disease_details": {
      "name": "Early Blight",
      "scientific_name": "Alternaria solani",
      "severity": "high",
      "symptoms": [...],
      "treatment": [...],
      "prevention": [...]
    }
  }
}
```

#### `GET /api/models`
- Returns model metadata including:
  - Framework: ONNX Runtime
  - Input size: [224, 224]
  - Number of classes: 38
  - Model path: `saved_models/model.onnx`

#### `GET /api/health`
- Health check endpoint (unchanged)

---

## Deployment Instructions

### 1. Verify Model Files
```bash
# Check that the ONNX model exists
ls -la saved_models/model.onnx
ls -la saved_models/plantvillage_run/final_metrics.json
```

### 2. Install Dependencies
```bash
pip install onnxruntime onnx
```

### 3. Start Backend
```bash
# From project root
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 4. Test Prediction
```bash
curl -X POST http://localhost:8000/api/predict \
  -F "image=@path/to/plant/leaf.jpg"
```

### 5. Verify Model Info
```bash
curl http://localhost:8000/api/models
```

---

## Performance Characteristics

### Inference Speed
- **Single Image (batch=1):** ~150-200 ms (GPU)
- **Batch of 32:** ~2-3 seconds (GPU)
- **Memory Usage:** ~1.2 GB VRAM
- **Model Size on Disk:** 103 MB (ONNX)

### Hardware Requirements
**Minimum:**
- CPU: 4 cores
- RAM: 8 GB
- Storage: 200 MB

**Recommended:**
- GPU: NVIDIA CUDA 11.0+ (2GB+ VRAM)
- CPU: 8+ cores
- RAM: 16 GB
- Storage: 500 MB

---

## Production Checklist

- [x] Model trained to 98%+ accuracy
- [x] Test set evaluation completed
- [x] ONNX export validated
- [x] PyTorch vs ONNX inference match rate: 100%
- [x] Backend updated to use ONNX Runtime
- [x] Mock fallback removed
- [x] API endpoints tested
- [x] Model metadata exported
- [x] Deployment documentation created
- [x] Class names and disease info available

---

## Known Limitations

1. **Image Requirements:**
   - Minimum size: 224×224 pixels
   - Optimal: 512×512 or larger
   - Format: RGB (JPEG, PNG, WebP)
   - Suggested: High-quality, well-lit photos

2. **Model Scope:**
   - Limited to 38 predefined disease classes
   - Requires clear leaf/plant tissue visible
   - Accuracy degrades with extremely poor image quality

3. **Inference:**
   - First prediction ~2-3 seconds (model load)
   - Subsequent predictions ~200ms (GPU)

---

## Future Improvements

1. **Model Enhancement:**
   - Ensemble multiple architectures (EfficientNet, Vision Transformer)
   - Add temporal tracking for disease progression
   - Fine-tune on domain-specific augmentations

2. **Deployment:**
   - Containerize with Docker for easy deployment
   - Add model versioning and A/B testing
   - Implement request rate limiting

3. **Monitoring:**
   - Log all predictions for retraining datasets
   - Track prediction confidence over time
   - Alert on unusual patterns

---

## Support & Troubleshooting

### Issue: ONNX Runtime not found
```bash
pip install --upgrade onnxruntime
```

### Issue: Model predictions vary between PyTorch and ONNX
- Run validation: `python evaluate_final_model.py`
- Verify input preprocessing matches exactly

### Issue: Slow inference
- Use GPU acceleration: Ensure CUDA is available
- Batch process if possible
- Monitor GPU memory usage

---

## Metadata & Traceability

| Property | Value |
|----------|-------|
| **PyTorch Checkpoint** | `best_head_model.pth` from Phase 1 training (Epoch 14) |
| **Export Date** | 2026-06-15 |
| **Export Tool** | `torch.onnx.export` with opset 14 |
| **Validation Status** | ✅ Passed (100% inference match) |
| **Training Framework** | PyTorch 2.0+ |
| **ONNX Runtime Version** | 1.26.0+ |
| **Python Version** | 3.8+ |

---

## Contact & Maintenance

For issues or questions:
1. Check the backend logs: `backend/logs/`
2. Run `evaluate_final_model.py` to validate model integrity
3. Review metrics in `saved_models/plantvillage_run/final_metrics.json`

---

**Report Generated:** 2026-06-15  
**Status:** ✅ PRODUCTION READY FOR DEPLOYMENT
