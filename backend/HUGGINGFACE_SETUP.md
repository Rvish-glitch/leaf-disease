# Hugging Face Model Upload Instructions

## Step 1: Create Hugging Face Account
1. Go to https://huggingface.co
2. Create an account
3. Go to https://huggingface.co/settings/tokens
4. Create a new token with "Write" permissions

## Step 2: Login to Hugging Face
```bash
# Install huggingface-hub if not already installed
pip install huggingface_hub

# Login with your token
huggingface-cli login
# or
hf auth login
```

## Step 3: Upload Your Model
```bash
# Edit upload_to_hf.py and change the repo_id to your username
# Then run:
python upload_to_hf.py
```

## Step 4: Update Environment Variable
After uploading to Hugging Face, update your Railway deployment:

1. Go to Railway dashboard
2. Click on your backend service
3. Go to "Variables" tab
4. Add environment variable:
   - Name: `HF_REPO_ID`
   - Value: `your-username/leaf-disease-detection`

## Alternative: Use Our Pre-uploaded Model
If you don't want to upload your own model, you can use a public repository.
Just set the HF_REPO_ID environment variable to point to any public model repository.

## Benefits of Using Hugging Face:
- No Git LFS issues
- Faster downloads
- Better caching
- No file size limits
- Automatic CDN distribution
- Version control for models
