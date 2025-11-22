# Deployment Troubleshooting Guide

## Current Issue: Non-zero exit code during installation

The error shows packages are installing but then failing with a non-zero exit code. This usually means:
1. A package failed to build/install
2. Memory/timeout during installation
3. Dependency conflict

## Solutions to Try

### Solution 1: Remove PyCaret (Recommended)

PyCaret is **NOT needed** for running the app - it's only used in `extract_model.py` for model extraction. The deployed app uses `joblib` to load models.

**Try this first:**

1. Create a new file `requirements-deploy.txt`:
   ```txt
   numpy==1.26.4
   pillow>=9.0.0,<11.0.0
   pandas>=1.5.0,<2.0.0
   scipy>=1.10.0,<1.12.0
   scikit-learn>=1.4.1,<1.5.0
   matplotlib>=3.7.0,<3.9.0
   seaborn>=0.12.2,<0.13.0
   opencv-python-headless>=4.8.0,<4.9.0
   xgboost>=1.7.0,<2.0.0
   joblib>=1.3.0
   torch>=2.1.0,<2.3.0
   ultralytics>=8.0.196,<8.2.0
   streamlit>=1.28.0,<1.33.0
   ```

2. Temporarily rename `requirements.txt` to `requirements-full.txt`
3. Rename `requirements-deploy.txt` to `requirements.txt`
4. Push and redeploy

### Solution 2: Use Specific Versions

Some packages might have version conflicts. Try pinning to specific working versions:

```txt
numpy==1.26.4
pandas==1.5.3
scipy==1.11.4
scikit-learn==1.4.2
matplotlib==3.7.5
seaborn==0.12.2
opencv-python-headless==4.8.1.78
xgboost==1.7.6
joblib==1.3.2
torch==2.1.2
ultralytics==8.1.47
streamlit==1.32.2
pillow==10.2.0
```

### Solution 3: Install in Stages

If the issue persists, the problem might be memory/timeout. Try splitting installation:

1. Create `requirements-base.txt` (core packages)
2. Create `requirements-ml.txt` (ML packages)
3. Use a custom build script (not supported by Streamlit Cloud directly)

### Solution 4: Check Build Logs

Look at the **full build logs** in Streamlit Cloud to see which package is actually failing. The error message should show:
- Which package failed
- What the actual error is
- Memory/timeout issues

### Solution 5: Alternative Hosting

If Streamlit Cloud continues to fail, consider:
- **Hugging Face Spaces** - Better for ML apps, more resources
- **Render** - More control over build process
- **Railway** - Better error messages

## Quick Fix Checklist

- [ ] Remove pycaret from requirements.txt
- [ ] Pin all versions to specific releases
- [ ] Check full build logs for actual error
- [ ] Try Hugging Face Spaces as alternative
- [ ] Verify model files are not too large

## Most Likely Fix

**Remove PyCaret** - It's not needed for deployment and has many heavy dependencies that might be causing the build to fail.

