# CropGuard - Full-Stack Plant Disease Detection

Professional SaaS-style AI application for detecting plant diseases using React, FastAPI, and ONNX inference.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
python main.py
```

Backend runs at `http://localhost:8000`
API docs available at `http://localhost:8000/docs`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

## 📁 Project Structure

```
plant_ai/
├── backend/                    # Python FastAPI Backend
│   ├── app/
│   │   ├── api/               # API routes & schemas
│   │   ├── models/            # ML predictor & disease database
│   │   ├── utils/             # Utilities
│   │   ├── config.py          # Configuration
│   │   └── main.py            # FastAPI app
│   ├── requirements.txt
│   └── main.py               # Entry point
│
├── frontend/                   # React + Vite Frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── hooks/             # Custom hooks
│   │   ├── services/          # API client
│   │   ├── context/           # Global state
│   │   ├── styles/            # CSS & animations
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── models/                     # Existing ML pipeline (UNCHANGED)
├── saved_models/              # Model checkpoints
├── data/                       # Training data
└── README.md                  # This file
```

## 🔗 API Endpoints

### Prediction
- `POST /api/predict` - Submit image for disease detection
- `GET /api/health` - Health check
- `GET /api/models` - Get model information

### Request Example
```bash
curl -X POST "http://localhost:8000/api/predict" \
  -H "accept: application/json" \
  -F "image=@path/to/image.jpg"
```

### Response Example
```json
{
  "success": true,
  "data": {
    "image_id": "uuid-string",
    "prediction": {
      "primary_disease": "Early Blight",
      "confidence": 0.9423
    },
    "top_3": [
      {
        "rank": 1,
        "disease_name": "Early Blight",
        "confidence": 0.9423,
        "color": "#FF6B6B"
      }
    ],
    "disease_details": {
      "name": "Early Blight",
      "symptoms": [...],
      "treatment": [...],
      "prevention": [...]
    }
  }
}
```

## 🎨 Features

✅ **Frontend**
- React 18 with modern hooks
- Vite for ultra-fast builds
- Tailwind CSS styling
- Framer Motion animations
- Dark mode support
- Responsive design
- Drag-and-drop file upload

✅ **Backend**
- FastAPI for high performance
- CORS enabled for frontend communication
- ONNX Runtime inference
- Comprehensive disease database
- Structured error handling
- Auto-generated API documentation

✅ **User Experience**
- Professional SaaS-style interface
- Real-time prediction visualization
- Confidence score charts
- Top 3 predictions ranking
- Disease symptoms & treatment info
- Prevention tips
- Mobile-friendly

## 🔧 Configuration

### Backend (.env)
```env
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

### Frontend (vite.config.js)
```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    }
  }
}
```

## 📊 Supported Diseases

- Healthy (no disease)
- Early Blight
- Late Blight
- Septoria Leaf Spot
- Yellow Leaf Curl Virus
- Bacterial Spot
- Target Spot

## 🔄 Data Flow

```
User uploads image (Frontend)
        ↓
File validation & preview
        ↓
POST /api/predict (multipart/form-data)
        ↓
Backend receives & validates
        ↓
ONNX model inference
        ↓
Top-3 predictions + disease details
        ↓
JSON response to frontend
        ↓
Animated results display
```

## 🧪 Testing

### Manual Testing
1. Start both backend and frontend
2. Navigate to `http://localhost:5173`
3. Upload a test plant image
4. Verify prediction and disease details

### API Testing
Use the built-in Swagger UI at `http://localhost:8000/docs`

## 🚀 Deployment

### Production Build (Frontend)
```bash
cd frontend
npm run build
# Output in frontend/dist/
```

### Production Run (Backend)
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Docker Compose
```bash
docker-compose up
```

## 📦 Dependencies

**Backend:**
- fastapi==0.104.1
- uvicorn
- torch & torchvision
- onnxruntime
- pydantic
- pillow
- opencv-python-headless

**Frontend:**
- react@18.2.0
- vite@5.0.8
- tailwindcss@3.4.1
- framer-motion@10.16.0
- axios@1.6.2
- react-router-dom@6.20.0

## 📝 License

MIT License - Feel free to use this project

## 🤝 Contributing

Contributions welcome! Please follow standard git workflow:
1. Create feature branch
2. Make changes
3. Submit pull request

## 📞 Support

For issues or questions, please open an issue on GitHub.

---

Built with ❤️ for farmers and agricultural professionals
