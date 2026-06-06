# CropGuard - Plant Disease Detection

CropGuard is a high-performance plant disease detection web application skeleton. It uses a transfer learning architecture with a ResNet-50 backbone, packaged as a lightweight ONNX model for CPU-optimized inference.

---

## 📂 Project Folder Structure & Responsibilities

```
plant_ai/
├── assets/                 # Brand logos, styling stylesheets, visual assets
│   └── .gitkeep
├── data/                   # Train/Val leaf image files organized by label subfolders
│   └── .gitkeep
├── models/                 # Model construction and prediction workflows
│   ├── __init__.py
│   ├── predict.py          # Placeholder class for model loading and ONNX predictions
│   └── train.py            # Placeholder functions for training and validation loaders
├── saved_models/           # Target destination directory for model checkpoint weights
│   └── .gitkeep
├── utils/                  # Core helpers and shared code modules
│   ├── __init__.py
│   └── image_processing.py # Image decoding, resizing, and float normalization utilities
├── config.py               # Global settings, learning rates, epochs, paths, and classes
├── README.md               # Skeletons overview, requirements, and run guide
└── requirements.txt        # Third-party module dependencies
```

---

## 🛠️ Description of Files

* **`config.py`**: A centralized configuration file to store training parameters, paths to datasets, model configuration keys, and classes names.
* **`models/train.py`**: Model setup script which loads transfer weights (ResNet-50), customizes classification output nodes, runs backpropagation, and outputs evaluation scores.
* **`models/predict.py`**: Inference pipeline implementing ONNX sessions, processing raw predictions, and pulling out Top-3 confidence candidates.
* **`utils/image_processing.py`**: OpenCV image functions to open image streams, resize matrices, convert color models, and normalize tensor floats.
* **`requirements.txt`**: Standard dependencies specifying library platforms (PyTorch, ONNX Runtime, OpenCV, Streamlit, etc.).
