"""
Comprehensive disease database with symptoms, treatments, and prevention tips.
Maps disease names to detailed agricultural information.
"""

DISEASE_DATABASE = {
    "Healthy": {
        "name": "Healthy",
        "scientific_name": "N/A",
        "severity": "none",
        "color": "#10B981",  # Green
        "symptoms": [
            "Plant appears normal and vigorous",
            "Leaves are green and firm",
            "No visible lesions or discoloration",
            "Stems are strong and upright"
        ],
        "treatment": [
            "Continue regular crop management",
            "Maintain proper irrigation schedule",
            "Monitor plant health regularly"
        ],
        "prevention": [
            "Practice crop rotation",
            "Use disease-resistant varieties",
            "Maintain good field hygiene",
            "Remove infected plants immediately"
        ],
        "description": "Your plant is healthy and thriving! Continue with your current care regimen."
    },
    "Early Blight": {
        "name": "Early Blight",
        "scientific_name": "Alternaria solani",
        "severity": "medium",
        "color": "#FF6B6B",  # Red
        "symptoms": [
            "Brown, concentric rings on lower leaves",
            "Yellow halo around lesions",
            "Lesions coalesce causing yellowing and dropping",
            "Primarily affects older, lower leaves first"
        ],
        "treatment": [
            "Remove infected leaves immediately",
            "Apply fungicide (Mancozeb, Chlorothalonil)",
            "Improve air circulation by pruning",
            "Water at soil level, avoid overhead watering",
            "Apply copper-based fungicides for severe cases"
        ],
        "prevention": [
            "Plant resistant varieties",
            "Practice crop rotation (2-3 year minimum)",
            "Mulch soil to prevent spore splash",
            "Stake plants for better air flow",
            "Remove plant debris after harvest",
            "Space plants properly for air circulation"
        ],
        "description": "Early blight is a fungal disease affecting older leaves first. Act quickly to prevent spread."
    },
    "Late Blight": {
        "name": "Late Blight",
        "scientific_name": "Phytophthora infestans",
        "severity": "high",
        "color": "#DC2626",  # Dark Red
        "symptoms": [
            "Water-soaked lesions on leaves and stems",
            "White moldy growth on undersides of leaves",
            "Rapid browning and decay of affected tissue",
            "Can affect entire plant within days",
            "Brown, sunken spots on fruits"
        ],
        "treatment": [
            "Remove infected plant parts immediately",
            "Apply protectant fungicides (copper, mancozeb)",
            "Use targeted fungicides (chlorothalonil, mefenoxam)",
            "Destroy severely infected plants",
            "Reduce leaf wetness and humidity",
            "Apply fungicides on 7-10 day schedule"
        ],
        "prevention": [
            "Plant resistant varieties (most effective)",
            "Provide good drainage",
            "Space plants for air circulation",
            "Avoid overhead irrigation",
            "Monitor closely during wet weather",
            "Remove volunteer plants and weeds",
            "Practice strict field sanitation"
        ],
        "description": "Late blight is highly destructive and spreads rapidly. Immediate action required!"
    },
    "Septoria Leaf Spot": {
        "name": "Septoria Leaf Spot",
        "scientific_name": "Septoria lycopersici",
        "severity": "medium",
        "color": "#FFA500",  # Orange
        "symptoms": [
            "Small circular lesions with dark borders",
            "Lesions have grayish-brown center",
            "Black specks (pycnidia) visible in center",
            "Yellow halo around lesions",
            "Primarily on lower and mid-canopy leaves",
            "Lesions gradually enlarge and coalesce"
        ],
        "treatment": [
            "Remove infected lower leaves",
            "Apply copper or chlorothalonil fungicides",
            "Improve air circulation and reduce humidity",
            "Water at base of plant, avoid wetting foliage",
            "Apply fungicide every 7-10 days in humid conditions"
        ],
        "prevention": [
            "Use disease-resistant varieties",
            "Practice 3-year crop rotation",
            "Space plants for good air flow",
            "Remove lower leaves when plants are small",
            "Mulch soil to prevent spore splash",
            "Destroy crop residue after harvest",
            "Disinfect pruning tools between cuts"
        ],
        "description": "Septoria leaf spot is a fungal disease that progressively affects lower leaves."
    },
    "Yellow Leaf Curl Virus": {
        "name": "Yellow Leaf Curl Virus",
        "scientific_name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "severity": "high",
        "color": "#FBBF24",  # Yellow
        "symptoms": [
            "Yellowing of leaf margins",
            "Upward curling of leaves",
            "Stunted plant growth",
            "Reduced fruit set and size",
            "Yellowing progresses inward from leaf edges",
            "Symptoms appear suddenly after transmission"
        ],
        "treatment": [
            "No cure - remove and destroy infected plants",
            "Control whitefly vectors with insecticides",
            "Use yellow sticky traps for monitoring",
            "Apply neem oil or insecticidal soap",
            "Maintain isolation from other susceptible crops"
        ],
        "prevention": [
            "Use resistant varieties (critical)",
            "Control whitefly populations aggressively",
            "Use reflective mulches to repel insects",
            "Place physical barriers (nets) over young plants",
            "Avoid planting near other host plants",
            "Use disease-free transplants",
            "Remove weeds that harbor whiteflies"
        ],
        "description": "Viral disease transmitted by whiteflies. Prevention is crucial - no cure available."
    },
    "Bacterial Spot": {
        "name": "Bacterial Spot",
        "scientific_name": "Xanthomonas spp.",
        "severity": "medium",
        "color": "#F97316",  # Deep Orange
        "symptoms": [
            "Small, dark, water-soaked spots on leaves",
            "Lesions develop yellow halo",
            "Spots may merge forming larger areas",
            "Affected tissue becomes necrotic and falls out",
            "Spots also appear on stems and fruits",
            "Lesions are raised and corky on fruit"
        ],
        "treatment": [
            "Remove infected leaves and plant parts",
            "Apply copper bactericides weekly",
            "Use antibiotic spray (streptomycin) if available",
            "Reduce plant density and improve air flow",
            "Water at soil level to keep foliage dry",
            "Avoid working in field when plants are wet"
        ],
        "prevention": [
            "Use disease-resistant varieties",
            "Practice 2-3 year crop rotation",
            "Use disease-free seeds and transplants",
            "Disinfect tools with bleach solution",
            "Remove plant debris promptly",
            "Space plants for good ventilation",
            "Avoid overhead irrigation"
        ],
        "description": "Bacterial disease spread by water and insects. Requires strict sanitation practices."
    },
    "Target Spot": {
        "name": "Target Spot",
        "scientific_name": "Corynespora cassiicola",
        "severity": "low_to_medium",
        "color": "#6366F1",  # Indigo
        "symptoms": [
            "Circular lesions with concentric rings",
            "Resembles target with 3-4 rings",
            "Small dark center surrounded by yellow halo",
            "Lesions primarily on lower leaves initially",
            "Can affect stems and fruits",
            "Develops slowly compared to other diseases"
        ],
        "treatment": [
            "Remove affected leaves",
            "Apply chlorothalonil or copper fungicides",
            "Reduce humidity and improve air circulation",
            "Avoid overhead watering",
            "Apply fungicide every 10-14 days in humid weather"
        ],
        "prevention": [
            "Use resistant varieties if available",
            "Maintain crop rotation",
            "Ensure proper plant spacing",
            "Mulch soil surface",
            "Remove plant residue after harvest",
            "Keep field free of weeds",
            "Maintain plant vigor with proper nutrition"
        ],
        "description": "Target spot is a fungal disease that develops slowly under warm, humid conditions."
    }

    ,
    "Apple Scab": {
        "name": "Apple Scab",
        "scientific_name": "Venturia inaequalis",
        "severity": "medium",
        "color": "#F59E0B",
        "symptoms": [
            "Olive-green to brown lesions on leaves",
            "Lesions on fruit causing scabby, corky areas",
            "Premature leaf drop in severe cases"
        ],
        "treatment": [
            "Remove and destroy fallen leaves and infected fruit",
            "Apply protective fungicides during leaf emergence",
            "Prune to improve air circulation and reduce humidity"
        ],
        "prevention": [
            "Plant resistant varieties where available",
            "Rake and destroy leaf litter each autumn",
            "Avoid overhead irrigation; water at soil level"
        ],
        "description": "Fungal disease that affects leaves and fruit; effective management reduces yield losses."
    },
    "Apple Black Rot": {
        "name": "Apple Black Rot",
        "scientific_name": "Botryosphaeria obtusa",
        "severity": "medium",
        "color": "#A855F7",
        "symptoms": [
            "Circular brown to black lesions on fruit",
            "Canker-like lesions on branches",
            "Leaf spots and early defoliation in severe infections"
        ],
        "treatment": [
            "Prune out and destroy dead or infected wood",
            "Remove mummified fruit from trees and ground",
            "Apply fungicides in high-pressure outbreak years"
        ],
        "prevention": [
            "Maintain tree vigor with proper nutrition and irrigation",
            "Sanitize pruning tools and remove infected debris",
            "Select disease-tolerant rootstocks or varieties when possible"
        ],
        "description": "A fungal disease causing fruit rot and branch cankers; sanitation is key."
    },
    "Cedar Apple Rust": {
        "name": "Cedar Apple Rust",
        "scientific_name": "Gymnosporangium juniperi-virginianae",
        "severity": "low_to_medium",
        "color": "#FB923C",
        "symptoms": [
            "Yellow-orange spots on upper leaf surfaces",
            "Fruiting bodies on underside of leaves and on nearby junipers",
            "Premature leaf drop in heavy infections"
        ],
        "treatment": [
            "Remove nearby juniper (cedar) hosts if practical",
            "Apply fungicide sprays during susceptible periods",
            "Prune out heavily infected leaves and twigs"
        ],
        "prevention": [
            "Avoid planting apple trees near junipers",
            "Use resistant apple varieties when available",
            "Monitor and remove early infections to reduce spread"
        ],
        "description": "A rust disease with a two-host lifecycle (juniper and apple); managing alternate hosts helps control it."
    },
    "Powdery Mildew": {
        "name": "Powdery Mildew",
        "scientific_name": "Various Erysiphaceae spp.",
        "severity": "low_to_medium",
        "color": "#C084FC",
        "symptoms": [
            "White powdery growth on leaf surfaces",
            "Distorted or curled new leaves",
            "Reduced photosynthesis and vigor in heavy cases"
        ],
        "treatment": [
            "Remove severely infected leaves",
            "Apply sulfur or potassium bicarbonate fungicides",
            "Improve air flow and reduce shade"
        ],
        "prevention": [
            "Space plants for good air circulation",
            "Avoid excessive nitrogen that encourages tender growth",
            "Choose resistant varieties when available"
        ],
        "description": "Common fungal disease on many crops; visible as white powdery patches on leaves."
    },
    "Cercospora Leaf Spot": {
        "name": "Cercospora Leaf Spot (Gray Leaf Spot)",
        "scientific_name": "Cercospora spp.",
        "severity": "medium",
        "color": "#EF4444",
        "symptoms": [
            "Rectangular or elongated gray-brown lesions on leaves",
            "Lesions often align with leaf veins",
            "Severe infections lead to premature leaf death"
        ],
        "treatment": [
            "Rotate crops and remove infected residue",
            "Apply appropriate fungicides during humid conditions",
            "Manage irrigation to reduce leaf wetness"
        ],
        "prevention": [
            "Use certified seed and resistant hybrids when possible",
            "Avoid overhead irrigation in humid climates",
            "Practice crop rotation and field sanitation"
        ],
        "description": "Fungal leaf spot disease common in corn; thrives in warm, wet conditions."
    },
    "Common Rust": {
        "name": "Common Rust",
        "scientific_name": "Puccinia sorghi",
        "severity": "low_to_medium",
        "color": "#F97316",
        "symptoms": [
            "Reddish-brown pustules (uredinia) on leaf surfaces",
            "Pustules can appear on both leaf sides",
            "Severe infections reduce photosynthetic area"
        ],
        "treatment": [
            "Select rust-resistant corn varieties",
            "Apply fungicides when disease pressure is high",
            "Remove volunteer corn that can harbor rust"
        ],
        "prevention": [
            "Rotate crops to non-host plants",
            "Use certified seed and maintain plant vigor",
            "Monitor and remove early outbreaks"
        ],
        "description": "A common rust of maize that produces orange-reddish pustules; manage with resistant varieties and sanitation."
    },
    "Northern Leaf Blight": {
        "name": "Northern Leaf Blight",
        "scientific_name": "Exserohilum turcicum",
        "severity": "medium",
        "color": "#F59E0B",
        "symptoms": [
            "Long, cigar-shaped gray-green to tan lesions on leaves",
            "Lesions enlarge and can merge under high disease pressure",
            "Reduced yield if foliar area is heavily affected"
        ],
        "treatment": [
            "Plant resistant hybrids when available",
            "Apply foliar fungicides if disease onset is early and severe",
            "Remove crop residue to reduce overwintering inoculum"
        ],
        "prevention": [
            "Rotate with non-host crops",
            "Use tillage or residue management to lower inoculum",
            "Monitor weather and apply timely fungicide where needed"
        ],
        "description": "Important foliar disease of corn; timing of control measures is critical to protect yield."
    },
    "Grape Black Rot": {
        "name": "Grape Black Rot",
        "scientific_name": "Guignardia bidwellii",
        "severity": "medium",
        "color": "#7C3AED",
        "symptoms": [
            "Small brown spots on leaves that expand and turn black",
            "Fruit develop sunken black lesions and mummify",
            "Infected shoots may show cankering in severe cases"
        ],
        "treatment": [
            "Remove and destroy mummified berries and infected canes",
            "Apply protectant fungicides during bloom and early season",
            "Improve canopy air flow through pruning"
        ],
        "prevention": [
            "Plant resistant cultivars when available",
            "Practice good sanitation and remove wild grape hosts",
            "Manage canopy to reduce humidity"
        ],
        "description": "Fungal disease causing rot on grapes; sanitation and early-season sprays reduce impact."
    },
    "Esca (Black Measles)": {
        "name": "Esca (Black Measles)",
        "scientific_name": "Complex of wood-invading fungi",
        "severity": "high",
        "color": "#DC2626",
        "symptoms": [
            "Dark, irregular lesions on grape berries (black measles)",
            "Leaf discoloration and tiger-striped patterns",
            "Wood decay and sudden vine collapse in advanced stages"
        ],
        "treatment": [
            "Remove and destroy severely infected vines",
            "Avoid excessive wounding during pruning",
            "Use balanced nutrition and avoid over-vigorous growth"
        ],
        "prevention": [
            "Use certified planting material free of trunk pathogens",
            "Sterilize pruning tools and avoid trunk wounds",
            "Monitor and remove symptomatic vines promptly"
        ],
        "description": "Complex trunk disease in grapes leading to berry symptoms and eventual vine decline."
    },
    "Leaf Blight (Isariopsis Leaf Spot)": {
        "name": "Leaf Blight (Isariopsis Leaf Spot)",
        "scientific_name": "Isariopsis spp.",
        "severity": "medium",
        "color": "#F97316",
        "symptoms": [
            "Small brown spots that coalesce into larger blighted areas",
            "Premature leaf yellowing and drop",
            "Reduced photosynthetic area leading to lower yields"
        ],
        "treatment": [
            "Apply appropriate fungicides during wet conditions",
            "Remove heavily infected leaves",
            "Improve air flow and reduce leaf wetness"
        ],
        "prevention": [
            "Practice good field sanitation",
            "Avoid overhead irrigation when possible",
            "Select tolerant varieties if available"
        ],
        "description": "Fungal leaf blight affecting grape foliage; manage humidity and apply fungicides as needed."
    },
    "Huanglongbing (Citrus Greening)": {
        "name": "Huanglongbing (Citrus Greening)",
        "scientific_name": "Candidatus Liberibacter spp.",
        "severity": "high",
        "color": "#B91C1C",
        "symptoms": [
            "Yellowing of leaves and blotchy mottle",
            "Small, lopsided, poorly colored fruit",
            "Tree decline and reduced yield over time"
        ],
        "treatment": [
            "No cure; remove and destroy infected trees",
            "Control the psyllid vector with insecticides",
            "Use disease-free nursery stock"
        ],
        "prevention": [
            "Monitor and control psyllid populations",
            "Plant certified disease-free saplings",
            "Implement area-wide management and rapid removal of infected trees"
        ],
        "description": "Serious bacterial disease of citrus spread by psyllids; prevention and rapid removal are essential."
    },
    "Leaf Scorch": {
        "name": "Leaf Scorch",
        "scientific_name": "Various causes (environmental or pathogenic)",
        "severity": "low_to_medium",
        "color": "#FDE68A",
        "symptoms": [
            "Brown or scorched leaf margins",
            "Leaves may curl or become brittle",
            "Often appears under drought or high-heat stress"
        ],
        "treatment": [
            "Improve irrigation to reduce drought stress",
            "Remove heavily affected foliage",
            "Address nutrient imbalances if present"
        ],
        "prevention": [
            "Maintain consistent soil moisture",
            "Mulch to conserve soil moisture and moderate temperatures",
            "Avoid over-fertilization that encourages stress-sensitive growth"
        ],
        "description": "Leaf scorch can result from environmental stress or pathogens; correct cultural issues to reduce occurrence."
    },
    "Leaf Mold": {
        "name": "Leaf Mold",
        "scientific_name": "Passalora fulva (on tomato)",
        "severity": "medium",
        "color": "#F59E0B",
        "symptoms": [
            "Yellow spots on upper leaf surface",
            "Grayish to olive mold growth on leaf undersides",
            "Leaves yellow and drop when infection is heavy"
        ],
        "treatment": [
            "Remove and destroy infected leaves",
            "Apply fungicides labeled for leaf mold control",
            "Improve ventilation in greenhouses and reduce humidity"
        ],
        "prevention": [
            "Space plants and prune to improve airflow",
            "Avoid overhead watering and keep foliage dry",
            "Use resistant tomato varieties when available"
        ],
        "description": "Fungal disease of tomato leaves favored by high humidity; environmental control is effective."
    },
    "Spider Mites (Two-spotted Spider Mite)": {
        "name": "Spider Mites (Two-spotted Spider Mite)",
        "scientific_name": "Tetranychus urticae",
        "severity": "low_to_medium",
        "color": "#F97316",
        "symptoms": [
            "Fine webbing on leaf undersides",
            "Yellow stippling and speckling on leaves",
            "Leaves may bronze and drop under heavy infestations"
        ],
        "treatment": [
            "Apply miticides or insecticidal soaps as labeled",
            "Introduce or conserve natural predators (predatory mites)",
            "Wash plants with strong water spray to dislodge mites"
        ],
        "prevention": [
            "Avoid plant stress; maintain adequate irrigation",
            "Monitor and use biological controls where possible",
            "Rotate miticides to prevent resistance"
        ],
        "description": "Tiny sap-sucking pests that cause stippling and webbing; biological control and careful miticide use are effective."
    },
    "Tomato Mosaic Virus": {
        "name": "Tomato Mosaic Virus",
        "scientific_name": "Tobamovirus (ToMV)",
        "severity": "medium",
        "color": "#FDE68A",
        "symptoms": [
            "Mottled, mosaic patterns on leaves",
            "Leaf distortion and stunting of young plants",
            "Reduced fruit set and quality"
        ],
        "treatment": [
            "No chemical cure; remove infected plants",
            "Disinfect tools and hands after handling plants",
            "Control weed hosts that may carry the virus"
        ],
        "prevention": [
            "Use certified virus-free seed and transplants",
            "Practice strict sanitation and disinfection",
            "Avoid tobacco use near production areas (tobacco can carry tobamoviruses)"
        ],
        "description": "A stable plant virus causing mottling and reduced yields; sanitation and clean material prevent spread."
    }
    ,
    # Aliases to handle dataset naming variations
    "Haunglongbing (Citrus Greening)": {
        "name": "Huanglongbing (Citrus Greening)",
        "scientific_name": "Candidatus Liberibacter spp.",
        "severity": "high",
        "color": "#B91C1C",
        "symptoms": [
            "Yellowing of leaves and blotchy mottle",
            "Small, lopsided, poorly colored fruit",
            "Tree decline and reduced yield over time"
        ],
        "treatment": [
            "No cure; remove and destroy infected trees",
            "Control the psyllid vector with insecticides",
            "Use disease-free nursery stock"
        ],
        "prevention": [
            "Monitor and control psyllid populations",
            "Plant certified disease-free saplings",
            "Implement area-wide management and rapid removal of infected trees"
        ],
        "description": "Alias entry to match dataset spelling variations for citrus greening."
    },
    "Spider Mites Two-spotted Spider Mite": {
        "name": "Spider Mites (Two-spotted Spider Mite)",
        "scientific_name": "Tetranychus urticae",
        "severity": "low_to_medium",
        "color": "#F97316",
        "symptoms": [
            "Fine webbing on leaf undersides",
            "Yellow stippling and speckling on leaves",
            "Leaves may bronze and drop under heavy infestations"
        ],
        "treatment": [
            "Apply miticides or insecticidal soaps as labeled",
            "Introduce or conserve natural predators (predatory mites)",
            "Wash plants with strong water spray to dislodge mites"
        ],
        "prevention": [
            "Avoid plant stress; maintain adequate irrigation",
            "Monitor and use biological controls where possible",
            "Rotate miticides to prevent resistance"
        ],
        "description": "Alias entry to match dataset naming for tomato spider mites variant."
    }
}


def get_disease_info(disease_name: str) -> dict:
    """
    Retrieve disease information from database.
    
    Args:
        disease_name: Name of the disease
        
    Returns:
        Dictionary with disease details, or default info if not found
    """
    # Exact match first
    if disease_name in DISEASE_DATABASE:
        return DISEASE_DATABASE[disease_name]

    # Normalization rules (to be tolerant of model class formatting)
    def _normalize(name: str) -> str:
        if not name or not isinstance(name, str):
            return ''
        # Remove the triple-underscore separator
        name = name.replace('___', ' ')
        # Replace underscores with spaces
        name = name.replace('_', ' ')
        # Collapse multiple spaces
        name = ' '.join(name.split())
        # Lowercase for normalized comparison
        return name.strip().lower()

    # Build normalized lookup mapping from database keys
    _normalized_db = { _normalize(k): v for k, v in DISEASE_DATABASE.items() }

    normalized_query = _normalize(disease_name)
    if normalized_query in _normalized_db:
        return _normalized_db[normalized_query]

    # Try replacing dashes with spaces and other minor variations
    alt = normalized_query.replace('-', ' ')
    if alt in _normalized_db:
        return _normalized_db[alt]

    # Attempt substring matching: class names often include plant name prefix
    # e.g., 'tomato late blight' should match DB key 'late blight'
    for db_norm, entry in _normalized_db.items():
        if db_norm in normalized_query or normalized_query in db_norm:
            return entry

    # Default fallback
    return {
        "scientific_name": "Unknown",
        "severity": "unknown",
        "color": "#6B7280",
        "symptoms": ["Unable to retrieve symptoms"],
        "treatment": ["Consult with agricultural expert"],
        "prevention": ["Follow general crop management practices"],
        "description": "Disease information not available in database"
    }
