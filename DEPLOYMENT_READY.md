# Deployment Guide

## Your repository is ready for deployment! 🚀

### GitHub Repository: https://github.com/Rvish-glitch/leaf-disease

## Backend Deployment on Railway

### Files Ready:
- ✅ `backend/requirements.txt` - All dependencies with specific versions
- ✅ `backend/runtime.txt` - Python 3.10.12
- ✅ `backend/Procfile` - Gunicorn configuration 
- ✅ `backend/app.py` - Production-ready Flask app
- ✅ Model file handled with Git LFS

### Railway Setup:
1. Go to [railway.app](https://railway.app)
2. Create new project from GitHub repo: `Rvish-glitch/leaf-disease`
3. Set root directory to: `backend`
4. Railway will auto-detect Python and use your Procfile

### Environment Variables (if needed):
- `PORT` - Automatically set by Railway
- `PYTHONPATH` - May need to set to `/app` if needed

## Frontend Deployment on Vercel

### Files Ready:
- ✅ `frontend/package.json` - React dependencies
- ✅ `frontend/vercel.json` - Vercel configuration
- ✅ `frontend/build/` - Production build files

### Vercel Setup:
1. Go to [vercel.com](https://vercel.com)
2. Import project from GitHub: `Rvish-glitch/leaf-disease`
3. Set root directory to: `frontend`
4. Build command: `npm run build`
5. Output directory: `build`

### Environment Variables for Frontend:
- `REACT_APP_API_URL` - Set to your Railway backend URL

## Tech Stack:
- **Backend**: Flask + TensorFlow 2.18.0 + Keras 3.5.0
- **Frontend**: React 
- **Model**: EfficientNetB3 (82MB via Git LFS)
- **Deployment**: Railway (backend) + Vercel (frontend)

## Next Steps:
1. Deploy backend on Railway
2. Get the Railway URL (e.g., `https://your-app.railway.app`)
3. Deploy frontend on Vercel
4. Set `REACT_APP_API_URL` in Vercel to your Railway URL
5. Test the complete application!

Your code is production-ready! 🎉
