# CropGuard Production Deployment Checklist

## Pre-Deployment Verification

### Code Quality
- [ ] All tests passing
- [ ] No console errors in frontend
- [ ] Linting passes (ESLint, Pylint)
- [ ] No hardcoded credentials or API keys
- [ ] Environment variables documented

### Security
- [ ] CORS properly configured for production domain
- [ ] HTTPS enabled on production
- [ ] Input validation on all endpoints
- [ ] File upload restrictions enforced
- [ ] No sensitive data in error messages
- [ ] Database/model credentials in .env files

### Performance
- [ ] Frontend bundle size acceptable (<1MB)
- [ ] Image optimization applied
- [ ] Lazy loading implemented
- [ ] API response times validated
- [ ] Database queries optimized

### Documentation
- [ ] README.md complete and accurate
- [ ] API documentation generated
- [ ] Deployment instructions clear
- [ ] Architecture diagram included
- [ ] Contributing guidelines documented

---

## Backend Deployment (Render)

### Step 1: Prepare Repository
```bash
# Ensure latest code is committed
git status
git add .
git commit -m "Production deployment"
git push origin main
```

### Step 2: Create Render Service
1. Visit https://render.com
2. Create new "Web Service"
3. Connect GitHub repository
4. Configure:
   - **Name**: cropguard-api
   - **Runtime**: Python 3.12
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python backend/main.py`
   - **Instance Type**: Starter (or Performance for higher throughput)

### Step 3: Set Environment Variables
In Render Dashboard → Environment:
```
PYTHON_UNBUFFERED=true
PORT=10000
DEBUG=False
HOST=0.0.0.0
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com,https://www.vercelapp.com
```

### Step 4: Deploy
- Render automatically deploys on push to main
- Monitor deployment logs in Render Dashboard
- Verify health check: `https://your-service.onrender.com/api/health`

### Step 5: Verification
```bash
# Test health endpoint
curl https://your-service.onrender.com/api/health

# Test prediction (with sample image)
curl -X POST https://your-service.onrender.com/api/predict \
  -F "file=@sample_image.jpg"
```

---

## Frontend Deployment (Vercel)

### Step 1: Prepare Frontend
```bash
cd frontend
npm install
npm run build
# Verify dist/ directory created
ls -la dist/
```

### Step 2: Create Vercel Project
1. Visit https://vercel.com
2. Create new project
3. Select GitHub repository
4. Configure:
   - **Framework**: Vite
   - **Root Directory**: `./frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### Step 3: Set Environment Variables
In Vercel Project Settings → Environment Variables:
```
VITE_API_URL=https://your-render-service.onrender.com/api
```

### Step 4: Deploy
- Vercel automatically deploys on push to main
- Monitor deployment in Vercel Dashboard
- Preview URL provided immediately

### Step 5: Configure Custom Domain
1. Add domain in Vercel Dashboard
2. Update DNS records
3. Enable HTTPS (automatic with Vercel)

---

## Post-Deployment Verification

### Health Checks
```bash
# Backend health
curl https://your-backend.onrender.com/api/health

# Frontend accessibility
curl https://your-domain.com

# API connectivity
curl -X POST https://your-backend.onrender.com/api/predict \
  -F "file=@test_image.jpg"
```

### User Acceptance Testing
- [ ] Landing page loads correctly
- [ ] Detection page responds quickly
- [ ] Image upload works
- [ ] Disease detection returns results
- [ ] Dark mode toggle works
- [ ] Mobile responsiveness verified
- [ ] No console errors
- [ ] Error messages are user-friendly

### Performance Monitoring
- [ ] Monitor API response times
- [ ] Check error rates
- [ ] Verify throughput expectations
- [ ] Monitor server resource usage

### Log Monitoring
**Backend (Render)**:
- Visit Render Dashboard → Logs
- Monitor for errors and warnings
- Check cold start times

**Frontend (Vercel)**:
- Visit Vercel Dashboard → Deployments
- Check build times
- Monitor real user analytics

---

## Maintenance Schedule

### Daily
- [ ] Check error rates in logs
- [ ] Monitor API health

### Weekly
- [ ] Review performance metrics
- [ ] Check deployment status
- [ ] Test full user flow

### Monthly
- [ ] Update dependencies
- [ ] Review security advisories
- [ ] Analyze usage patterns
- [ ] Optimize slow endpoints

### Quarterly
- [ ] Major version updates
- [ ] Conduct security audit
- [ ] Performance review and optimization

---

## Scaling Guidelines

### When to Scale
- Backend: >200 concurrent users or >500ms response times
- Frontend: >100 million requests/month

### Scaling Options

**Backend (Render)**:
```
Starter → Standard → Pro → Premium
- Increase vCPU allocation
- Increase RAM
- Add caching layer (Redis)
- Database optimization
```

**Frontend (Vercel)**:
- Vercel automatically scales globally
- No manual scaling needed
- Consider Edge Middleware for custom logic

---

## Troubleshooting

### Backend Won't Start
```bash
# Check logs
git push origin main  # Retrigger deploy
# Check environment variables in Render
# Verify model file exists: backend/saved_models/model.onnx
```

### High API Response Times
- Check Render CPU/RAM usage
- Optimize image processing
- Enable ONNX optimizations
- Consider batch processing API

### Frontend Not Connecting to Backend
- Verify VITE_API_URL environment variable
- Check CORS configuration in backend
- Verify backend is running
- Check browser console for CORS errors

### Model Loading Fails
- Verify model path in config
- Check file permissions
- Ensure 93.67 MB model file present
- Check available disk space on Render

---

## Rollback Procedure

### If Deployment Has Critical Issues

**Backend (Render)**:
1. Go to Render Dashboard
2. Select CropGuard service
3. Click "Manual Deploy"
4. Select previous stable commit

**Frontend (Vercel)**:
1. Go to Vercel Dashboard
2. Select Deployments
3. Click "Rollback" next to previous version

---

## Security Checklist

### Before Going Live
- [ ] Remove all debug print statements
- [ ] Disable DEBUG mode in production
- [ ] Verify CORS whitelist correct
- [ ] Remove example credentials
- [ ] Enable HTTPS everywhere
- [ ] Set secure cookies (if applicable)
- [ ] Configure rate limiting
- [ ] Test file upload restrictions
- [ ] Verify error messages don't leak system info
- [ ] Security headers configured

### Ongoing Security
- [ ] Regular dependency updates
- [ ] Monitor for CVE advisories
- [ ] Review access logs
- [ ] Implement intrusion detection
- [ ] Regular security audits

---

## Documentation References

- Render Docs: https://render.com/docs
- Vercel Docs: https://vercel.com/docs
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/
- React Production Build: https://react.dev/learn/start-a-new-react-project

---

**Deployment Date**: _______________  
**Deployed By**: _______________  
**Status**: ☐ Staging | ☐ Production

