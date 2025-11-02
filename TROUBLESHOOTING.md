# Troubleshooting Streamlit Cloud Deployment

## Issue: "Permission denied (publickey)" or "Failed to download Git LFS files"

### Solution 1: Make Repository Public (CRITICAL - Do This First!)

**This is the most important step!** Streamlit Cloud needs public access to download Git LFS files via HTTPS.

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

### Solution 3: Verify Git LFS Configuration

The repository now includes `.lfsconfig` which forces Git LFS to use HTTPS:

1. Verify `.lfsconfig` file exists in your repository and contains:
   ```
   [lfs]
       url = https://github.com/mtaha-23/finetuning-pseudocode-to-python.git/info/lfs
   ```

2. Verify `.gitattributes` file exists and contains:
   ```
   *.safetensors filter=lfs diff=lfs merge=lfs -text
   ```

3. Check repository on GitHub to ensure model file shows "Stored with Git LFS"

### Solution 4: Reboot Streamlit Cloud App

After making the repository public and ensuring `.lfsconfig` is committed:
1. Go to your Streamlit Cloud dashboard
2. Click the **⋮** (three dots) menu on your app
3. Select **Reboot app**
4. Wait for it to redeploy

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

