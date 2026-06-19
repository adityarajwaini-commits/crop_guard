# CropGuard Performance Optimization Guide

## Current Performance Metrics
- Model Inference: ~500ms per image
- API Response Time: <1s end-to-end
- Model Size: 93.67 MB
- Throughput: 120 predictions/minute on standard CPU

## Optimization Recommendations

### 1. ONNX Runtime Optimization (Backend)

**Location**: `models/onnx_predictor.py`

```python
import onnxruntime as ort

# Current (baseline)
self.session = ort.InferenceSession(model_path)

# Optimized
sess_options = ort.SessionOptions()
sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
sess_options.intra_op_num_threads = 4  # Match CPU cores

# Use CPU providers with optimizations
providers = [
    ('CPUExecutionProvider', {'
        'arena_extend_strategy': 'kSameAsRequested',
        'inter_op_num_threads': 4
    })
]

self.session = ort.InferenceSession(model_path, sess_options, providers)
```

**Benefits**: 15-20% inference speed improvement

### 2. Image Processing Pipeline Optimization

**Location**: `models/onnx_predictor.py` - `preprocess()` method

```python
# Use OpenCV instead of Pillow for faster processing
import cv2

def preprocess_optimized(self, image_bytes):
    """Optimized preprocessing with OpenCV"""
    import io
    from PIL import Image
    
    # Decode image
    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    
    # OpenCV faster resize
    img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_LINEAR)
    
    # BGR to RGB (OpenCV uses BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Normalization
    img = img / 255.0
    img = (img - np.array([0.485, 0.456, 0.406])) / np.array([0.229, 0.224, 0.225])
    
    return np.transpose(img, (2, 0, 1))[np.newaxis, :].astype(np.float32)
```

**Benefits**: 30-40% image processing speed improvement

### 3. Model Lazy Loading & Caching

**Location**: `backend/app/api/routes.py`

Current implementation uses lazy loading which is good. Ensure:
- Model loaded once at first request
- Singleton pattern prevents reloads
- In-memory caching across requests

### 4. Frontend Optimization

**Location**: `frontend/src/services/api.js`

```javascript
// Add request timeout
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,  // 30s timeout
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

// Add response interceptor for caching
api.interceptors.response.use(
  (response) => {
    // Cache disease info responses (TTL: 1 hour)
    if (response.config.url.includes('/api/diseases')) {
      localStorage.setItem(
        `cache_${response.config.url}`,
        JSON.stringify({ data: response.data, timestamp: Date.now() })
      );
    }
    return response;
  }
);
```

### 5. Database Query Optimization

**Location**: `backend/app/models/disease_database.py`

- Cache disease info in-memory on startup
- Use dictionary lookups (O(1)) instead of linear search
- Pre-compute disease class mappings

### 6. API Response Compression

**Location**: `backend/app/main.py`

Already implemented with GZipMiddleware. Ensure:
```python
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### 7. Batch Processing (Future Enhancement)

For high-load scenarios:
```python
@router.post("/predict/batch")
async def batch_predict(files: List[UploadFile] = File(...)):
    """Batch prediction endpoint for multiple images"""
    # Process multiple images in one session
    # Reduces model loading overhead
```

### 8. Caching Headers

**Location**: `backend/app/main.py`

```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cache import CacheControlMiddleware

# Add cache control for static assets
@app.get("/api/models")
async def get_models():
    response = JSONResponse(content={...})
    response.headers["Cache-Control"] = "public, max-age=3600"
    return response
```

## Deployment Performance Tips

### 1. Render Backend
- Use "Performance" tier for better CPU allocation
- Monitor and scale based on demand
- Set appropriate worker threads (default: 4)

### 2. Vercel Frontend
- Vercel automatically optimizes builds
- Use serverless functions for API proxy if needed
- Enable edge caching

### 3. Docker Optimization
```dockerfile
# Use official Python slim image
FROM python:3.12-slim

# Multi-stage build to reduce image size
RUN pip install --no-cache-dir -r requirements.txt
```

## Monitoring & Metrics

Track these metrics:
- Average inference time per request
- API response time (P50, P95, P99)
- Model loading time
- Memory usage
- Throughput (requests/minute)

Use tools:
- **Backend**: Python logging, APM tools
- **Frontend**: Web Vitals, Sentry
- **Monitoring**: Render logs, Vercel Analytics

## Load Testing

```bash
# Using Apache Bench
ab -n 100 -c 10 http://localhost:8000/api/health

# Using wrk
wrk -t4 -c100 -d30s http://localhost:8000/api/health
```

## Quick Wins (Implement First)

1. ✓ ONNX session optimization (15-20% speedup)
2. ✓ Image processing with OpenCV (30-40% speedup)
3. ✓ Disease info caching (eliminate redundant lookups)
4. ✓ Frontend response caching (instant local responses)
5. ✓ Verify GZip middleware active (reduce payload)

## Benchmarking Commands

```bash
# Test API response time
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/api/health

# Frontend bundle size
npm run build && ls -lh frontend/dist/

# Backend performance
python -m cProfile -s cumulative backend/main.py
```

---

**Expected Performance After Optimizations:**
- Inference: 300-400ms (from 500ms)
- API Response: 400-700ms total (from <1s)
- Throughput: 150-200 predictions/minute (from 120)
