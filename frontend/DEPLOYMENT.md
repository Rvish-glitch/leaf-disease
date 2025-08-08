# Deployment Guide for Vercel

## Prerequisites
1. Install Vercel CLI: `npm i -g vercel`
2. Make sure you have a GitHub account
3. Your backend API should be deployed separately (e.g., on Railway, Render, or Heroku)

## Step 1: Deploy Backend First
Before deploying the frontend, you need to deploy your Flask backend to a platform that supports Python:

### Option A: Railway (Recommended)
1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Select the `backend` folder
4. Add environment variables if needed
5. Deploy

### Option B: Render
1. Go to [render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `python app.py`
6. Deploy

## Step 2: Deploy Frontend to Vercel

### Method 1: Using Vercel CLI
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy:
   ```bash
   vercel
   ```

4. Follow the prompts:
   - Set up and deploy: Yes
   - Which scope: Select your account
   - Link to existing project: No
   - Project name: leaf-disease-frontend (or your preferred name)
   - Directory: ./ (current directory)

### Method 2: Using Vercel Dashboard
1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Set the root directory to `frontend`
5. Configure build settings:
   - Build Command: `npm run build`
   - Output Directory: `build`
   - Install Command: `npm install`

## Step 3: Configure Environment Variables
After deployment, you need to set the backend API URL:

1. Go to your Vercel project dashboard
2. Navigate to Settings > Environment Variables
3. Add a new variable:
   - Name: `REACT_APP_API_URL`
   - Value: Your deployed backend URL (e.g., `https://your-backend.railway.app`)
4. Redeploy the project

## Step 4: Update CORS in Backend
Make sure your backend allows requests from your Vercel domain:

```python
# In your backend/app.py
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:3000",  # Local development
    "https://your-frontend.vercel.app"  # Your Vercel domain
])
```

## Step 5: Test Deployment
1. Visit your Vercel deployment URL
2. Upload a test image
3. Verify that predictions are working

## Troubleshooting

### Common Issues:
1. **CORS Errors**: Make sure your backend CORS settings include your Vercel domain
2. **API Connection**: Verify the `REACT_APP_API_URL` environment variable is set correctly
3. **Build Errors**: Check that all dependencies are in `package.json`
4. **Image Loading**: Ensure all static assets are in the `public` folder

### Environment Variables Reference:
- `REACT_APP_API_URL`: Your deployed backend API URL

### Build Commands:
- Build: `npm run build`
- Start (local): `npm start`
- Test: `npm test` 