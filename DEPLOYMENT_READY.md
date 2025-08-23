# Deployment Guide

## Your repository is ready for deployment! 🚀

### GitHub Repository: https://github.com/Rvish-glitch/leaf-disease

## Backend Deployment on Railway ✅ DEPLOYED

### URL: https://leaf-disease-production.up.railway.app

### Files Ready:
- ✅ `backend/requirements.txt` - All dependencies with specific versions
- ✅ `backend/runtime.txt` - Python 3.10.12
- ✅ `backend/Procfile` - Gunicorn configuration 
- ✅ `backend/app.py` - Production-ready Flask app with CORS
- ✅ Model file handled with Git LFS
- ✅ `backend/nixpacks.toml` - Git LFS support

## Frontend Deployment on Vercel ✅ READY

### Files Ready:
- ✅ `frontend/package.json` - React dependencies
- ✅ `frontend/vercel.json` - Vercel configuration
- ✅ `frontend/.env` - Production environment variables
- ✅ `frontend/.env.local` - Development environment variables
- ✅ API calls configured for production

### Vercel Setup:
1. Go to [vercel.com](https://vercel.com)
2. Import project from GitHub: `Rvish-glitch/leaf-disease`
3. Set root directory to: `frontend`
4. Build command: `npm run build`
5. Output directory: `build`
6. **Environment Variables will be auto-loaded from .env file**

## Environment Configuration:

### Production (Vercel):
- `REACT_APP_API_URL=https://leaf-disease-production.up.railway.app`

### Development (Local):
- `REACT_APP_API_URL=http://localhost:5000`

## CORS Configuration:
Backend allows requests from:
- ✅ `http://localhost:3000` (local development)
- ✅ `https://*.vercel.app` (Vercel deployments)
- ✅ `https://vercel.app` (Vercel domain)

## Tech Stack:
- **Backend**: Flask + TensorFlow 2.18.0 + Keras 3.5.0
- **Frontend**: React 
- **Model**: EfficientNetB3 (82MB via Git LFS)
- **Deployment**: Railway (backend) + Vercel (frontend)

## URLs:
- **Backend API**: https://leaf-disease-production.up.railway.app
- **Frontend**: Deploy on Vercel to get URL

## Testing:
- **Health Check**: GET https://leaf-disease-production.up.railway.app/
- **Prediction**: POST https://leaf-disease-production.up.railway.app/predict

Your production deployment is ready! 🎉
