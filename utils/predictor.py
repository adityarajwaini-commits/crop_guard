"""
Mock inference engine.
──────────────────────
Replace `mock_predict()` with your real model call.
The rest of the code reads from DISEASE_DB; add entries as your model grows.
"""

import random
import time
from datetime import datetime

# ── Disease knowledge base ────────────────────────────────────────────────────
DISEASE_DB = {
    "Tomato Late Blight": {
        "plant": "Tomato",
        "pathogen": "Phytophthora infestans (oomycete)",
        "severity": "high",
        "description": (
            "Late blight is one of the most destructive diseases of tomato and potato worldwide. "
            "It caused the 19th-century Irish Potato Famine. Lesions appear as water-soaked, "
            "pale-green to dark-brown patches that enlarge rapidly under cool, moist conditions. "
            "White sporulation is visible on the underside of leaves."
        ),
        "symptoms": [
            "Water-soaked lesions on leaves that turn brown-black",
            "White fuzzy sporulation on leaf undersides in humid weather",
            "Dark greasy lesions on stems and petioles",
            "Firm, brown lesions on fruit that spread rapidly",
        ],
        "treatment": [
            "Apply copper-based or chlorothalonil fungicides preventively",
            "Use systemic fungicides (mefenoxam, cymoxanil) at first symptom",
            "Remove and destroy infected plant material immediately",
            "Improve air circulation by pruning lower leaves",
            "Avoid overhead irrigation; use drip irrigation instead",
        ],
        "prevention": [
            "Plant resistant varieties (e.g., Mountain Magic, Defiant)",
            "Maintain 60–75 cm spacing between plants",
            "Rotate crops — avoid solanaceous crops for 3+ years",
            "Scout weekly, especially during cool rainy spells",
        ],
    },
    "Tomato Early Blight": {
        "plant": "Tomato",
        "pathogen": "Alternaria solani (fungus)",
        "severity": "medium",
        "description": (
            "Early blight is a common fungal disease appearing on older/stressed plants first. "
            "Characteristic concentric ring lesions (target-board pattern) distinguish it from "
            "other foliar diseases. Infection progresses from the bottom of the plant upward."
        ),
        "symptoms": [
            "Dark brown spots with concentric rings (target-board pattern)",
            "Yellow halo surrounding lesions",
            "Starts on older, lower leaves and progresses upward",
            "Stem lesions (collar rot) at or near the soil line in seedlings",
        ],
        "treatment": [
            "Apply chlorothalonil, mancozeb, or azoxystrobin fungicides",
            "Begin sprays when first symptoms appear; repeat every 7–10 days",
            "Remove heavily infected leaves to reduce inoculum",
            "Stake plants to improve air circulation",
        ],
        "prevention": [
            "Mulch around base to prevent soil splash",
            "Water at base, avoid wetting foliage",
            "Maintain adequate nitrogen fertilisation",
            "Use certified disease-free seed",
        ],
    },
    "Corn Northern Leaf Blight": {
        "plant": "Corn / Maize",
        "pathogen": "Exserohilum turcicum (fungus)",
        "severity": "medium",
        "description": (
            "Northern leaf blight produces long, cigar-shaped grey-green to tan lesions on corn "
            "leaves. Heavy infection before silking can cause 30–50% yield loss. The disease "
            "thrives in moderate temperatures with prolonged leaf wetness."
        ),
        "symptoms": [
            "Long elliptical grey-green or tan lesions (2.5–15 cm)",
            "Dark-sporulating lesions under humid conditions",
            "Lesions on lower leaves first, spreading upward",
            "Premature drying and death of entire leaves",
        ],
        "treatment": [
            "Apply foliar fungicides (azoxystrobin, propiconazole) at VT/R1 stage",
            "Fungicide timing is critical — spray before tasseling for best ROI",
        ],
        "prevention": [
            "Plant resistant hybrids with Ht genes",
            "Till crop residue to reduce overwintering inoculum",
            "Avoid planting corn-on-corn in disease-prone fields",
            "Balanced nitrogen fertility improves plant resilience",
        ],
    },
    "Apple Scab": {
        "plant": "Apple",
        "pathogen": "Venturia inaequalis (fungus)",
        "severity": "high",
        "description": (
            "Apple scab is the most economically important disease of apples worldwide. Olive-green "
            "to black velvety lesions appear on leaves and fruit surfaces. Infected fruit becomes "
            "cracked and deformed, rendering it unmarketable."
        ),
        "symptoms": [
            "Olive-green velvety lesions on upper leaf surface",
            "Yellowing and premature leaf drop",
            "Dark, scabby lesions on fruit surface",
            "Cracking and deformity of heavily infected fruit",
        ],
        "treatment": [
            "Apply captan, myclobutanil, or difenoconazole fungicides",
            "Start sprays at green-tip and continue through petal fall",
            "Use the RIMpro or MARYBLYT model to time sprays to infection periods",
            "Remove and dispose of fallen leaves in autumn",
        ],
        "prevention": [
            "Plant scab-resistant cultivars (e.g., Liberty, Redfree, GoldRush)",
            "Prune to open tree canopy for better air circulation",
            "Rake and destroy fallen leaves to eliminate overwintering spores",
        ],
    },
    "Grape Black Rot": {
        "plant": "Grape",
        "pathogen": "Guignardia bidwellii (fungus)",
        "severity": "high",
        "description": (
            "Black rot can destroy entire grape crops in wet seasons. Reddish-brown lesions with "
            "dark borders appear on leaves; infected berries turn brown then shrivel into hard black "
            "mummies that remain attached and serve as inoculum sources."
        ),
        "symptoms": [
            "Small reddish-brown leaf lesions with dark borders and tiny black pycnidia",
            "Berries turn brown, shrivel and mummify on the cluster",
            "Lesions on shoot tips, tendrils, and leaf petioles",
        ],
        "treatment": [
            "Apply mancozeb, myclobutanil, or tebuconazole from early shoot growth",
            "Critical spray window: 2 weeks pre-bloom through 4 weeks post-bloom",
            "Remove mummified berries and infected canes during winter pruning",
        ],
        "prevention": [
            "Choose resistant varieties where available",
            "Train vines to maximise air circulation and sun exposure",
            "Remove all mummies and debris before bud break",
        ],
    },
    "Healthy Plant": {
        "plant": "Various",
        "pathogen": "None detected",
        "severity": "healthy",
        "description": (
            "The leaf appears healthy with no visible signs of disease, pest damage, or nutritional "
            "deficiency. Continue your current management practices and monitor regularly."
        ),
        "symptoms": [
            "Uniform green coloration across the leaf blade",
            "No spots, lesions, or discolouration",
            "Healthy leaf margins and no wilting",
        ],
        "treatment": [
            "No treatment required — maintain current practices",
            "Ensure adequate irrigation and balanced fertilisation",
        ],
        "prevention": [
            "Scout regularly (at least weekly) for early disease detection",
            "Maintain plant nutrition — stressed plants are more susceptible",
            "Practice good sanitation: remove weeds and debris",
            "Rotate crops annually where possible",
        ],
    },
}

ALL_DISEASES = list(DISEASE_DB.keys())
PLANTS = ["Tomato", "Corn", "Apple", "Grape", "Potato", "Wheat", "Rice", "Soybean"]


# ── Class name normalization helper ───────────────────────────────────────────
def _normalize_class_name(name: str) -> str:
    if not name:
        return "Healthy Plant"
    
    # Replace underscores/hyphens with spaces, remove duplicate spaces
    clean_name = name.replace("_", " ").replace("-", " ").strip()
    clean_name = " ".join(clean_name.split())
    
    # Check for direct case-insensitive match
    for db_key in DISEASE_DB.keys():
        if clean_name.lower() == db_key.lower():
            return db_key
            
    # Handle healthy/normal aliases
    if clean_name.lower() in ["healthy", "healthy plant", "normal"]:
        return "Healthy Plant"
        
    # Check if a key contains the clean name, or vice versa
    for db_key in DISEASE_DB.keys():
        if clean_name.lower() in db_key.lower() or db_key.lower() in clean_name.lower():
            return db_key
            
    if "healthy" in clean_name.lower():
        return "Healthy Plant"
        
    # Fallback: title case the clean name
    return " ".join(word.capitalize() for word in clean_name.split())


# ── Mock inference fallback ───────────────────────────────────────────────────
def run_fallback_mock_predict() -> dict:
    """
    Simulate model inference.
    """
    time.sleep(1.2)          # simulate GPU latency

    primary = random.choice(ALL_DISEASES)
    conf    = round(random.uniform(0.72, 0.97), 4)

    # top-3
    others   = [d for d in ALL_DISEASES if d != primary]
    top3_raw = random.sample(others, min(2, len(others)))
    remaining = round(1 - conf, 4)
    top3_confs = sorted(
        [round(random.uniform(0.01, remaining * 0.8), 4) for _ in top3_raw],
        reverse=True,
    )
    top3 = [(primary, conf)] + list(zip(top3_raw, top3_confs))

    return {
        "disease":    primary,
        "confidence": conf,
        "top3":       top3,
        "info":       DISEASE_DB.get(primary, DISEASE_DB["Healthy Plant"]),
        "timestamp":  datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


# ── Predictor Setup ────────────────────────────────────────────────────────────
import streamlit as st
import os
import io
from PIL import Image

@st.cache_resource
def get_onnx_predictor(model_path: str):
    from onnx_predict import ONNXCropGuardPredictor
    return ONNXCropGuardPredictor(onnx_model_path=model_path)


# ── Core entry point for prediction ───────────────────────────────────────────
def mock_predict(image_bytes: bytes) -> dict:
    """
    Predict using real ONNX model if available, otherwise fall back to mock prediction.
    """
    model_path = os.path.join("saved_models", "model.onnx")
    
    if not os.path.exists(model_path):
        st.warning(
            "⚠️ CropGuard ONNX model not found at 'saved_models/model.onnx'. "
            "Running in simulation mode with mock predictions. "
            "To run real inference, please train a model and export it to ONNX format."
        )
        return run_fallback_mock_predict()
        
    try:
        # Load ONNX predictor (cached)
        predictor = get_onnx_predictor(model_path)
        
        # Load image from bytes
        image = Image.open(io.BytesIO(image_bytes))
        
        # Run prediction
        pred_res = predictor.predict(image, top_k=3)
        
        # Extract main prediction
        raw_disease = pred_res["disease_name"]
        raw_conf = pred_res["confidence"]
        
        # Normalize name to match DISEASE_DB keys
        disease = _normalize_class_name(raw_disease)
        confidence = round(float(raw_conf), 4)
        
        # Parse top 3 predictions
        top3 = []
        for item in pred_res.get("top_3_predictions", []):
            norm_name = _normalize_class_name(item["class_name"])
            item_conf = round(float(item["confidence"]), 4)
            top3.append((norm_name, item_conf))
            
        # Ensure the primary prediction is in the list
        if not any(d == disease for d, _ in top3):
            top3 = [(disease, confidence)] + top3[:2]
            
        info = DISEASE_DB.get(disease, DISEASE_DB["Healthy Plant"])
        
        return {
            "disease":    disease,
            "confidence": confidence,
            "top3":       top3,
            "info":       info,
            "timestamp":  datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        
    except Exception as e:
        st.warning(
            f"⚠️ Error during ONNX model inference: {str(e)}. "
            "Falling back to simulation mode."
        )
        return run_fallback_mock_predict()


def get_confidence_color(conf: float) -> str:
    if conf >= 0.85:
        return "#3fb950"
    if conf >= 0.65:
        return "#f0883e"
    return "#f85149"


def get_severity_badge(severity: str) -> str:
    mapping = {
        "high":    ("badge-high",    "⚠ HIGH RISK"),
        "medium":  ("badge-medium",  "⚡ MODERATE"),
        "low":     ("badge-low",     "✓ LOW RISK"),
        "healthy": ("badge-healthy", "✓ HEALTHY"),
    }
    cls, label = mapping.get(severity, ("badge-low", severity.upper()))
    return f'<span class="badge {cls}">{label}</span>'


HEALTHY_TIPS = [
    "🌱 Scout crops at least twice a week — catching diseases early cuts treatment costs by 60%.",
    "💧 Water at the base; wet foliage is the #1 driver of fungal disease.",
    "✂️ Prune to improve air circulation — stagnant air equals fungal paradise.",
    "🧪 Test soil annually; imbalanced nutrition weakens plant defences.",
    "🔄 Rotate crops yearly to break disease and pest cycles.",
    "🌿 Use certified disease-free seed and transplants.",
    "🏷️ Keep a field diary — patterns in disease outbreaks reveal spray timing opportunities.",
    "☀️ Increase plant spacing in high-humidity regions to reduce leaf wetness duration.",
]
