# Troubleshooting Streamlit Cloud Deployment

## Issue: "Failed to download the sources for repository"

### Solution 1: Make Repository Public (Most Common Fix)

1. Go to your GitHub repository: https://github.com/mtaha-23/finetuning-pseudocode-to-python
2. Click on **Settings** (top right)
3. Scroll down to **Danger Zone** section
4. Click **Change visibility** → **Make public**
5. Confirm the change
6. Go back to Streamlit Cloud and click **Reboot** on your app

### Solution 2: Grant Streamlit Cloud Access (If Keeping Private)

1. Go to GitHub → Settings → Applications → Authorized OAuth Apps
2. Find "Streamlit Cloud"
3. Ensure it has access to your repositories
4. Go back to Streamlit Cloud and click **Reboot**

### Solution 3: Check Git LFS (If Model File Issues)

Streamlit Cloud should handle Git LFS automatically, but if issues persist:

1. Verify `.gitattributes` file exists and contains:
   ```
   *.safetensors filter=lfs diff=lfs merge=lfs -text
   ```

2. Check repository on GitHub to ensure model file shows "Stored with Git LFS"

3. If Git LFS isn't working, try:
   ```bash
   git lfs pull
   git push origin main
   ```

### Solution 4: Alternative - Use Cloud Storage

If Git LFS continues to cause issues, you can host the model file elsewhere:
- Google Drive (public link)
- Hugging Face Hub
- AWS S3
- GitHub Releases

Then modify `app.py` to download at runtime.

## Verification Steps

1. ✅ Repository is public or Streamlit has access
2. ✅ Branch name is correct (`main`)
3. ✅ Main file path is correct (`app.py`)
4. ✅ All files are committed and pushed
5. ✅ Git LFS is properly configured (if using large files)

## Still Having Issues?

1. Check Streamlit Cloud logs for specific error messages
2. Verify repository URL is correct
3. Try deleting and recreating the Streamlit Cloud app
4. Check if GitHub repository is accessible via browser

