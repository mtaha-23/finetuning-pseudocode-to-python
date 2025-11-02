# Pseudocode to Python Generator - Streamlit App

A Streamlit web application for converting pseudocode to Python code using a fine-tuned GPT-2 model.

## Features

- 🐍 Convert pseudocode to Python code using fine-tuned GPT-2 model
- ⚙️ Adjustable generation parameters (temperature, top-p, max length)
- 🎨 Clean and intuitive user interface
- 📋 One-click code copying
- 💻 GPU support (CUDA) when available

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure model files are in the same directory:**
   - `model.safetensors` (or `pytorch_model.bin`)
   - `config.json`
   - `tokenizer_config.json`
   - `vocab.json`
   - `merges.txt`
   - `special_tokens_map.json`
   - `generation_config.json` (optional)

3. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

   The app will open in your default web browser at `http://localhost:8501`

## Usage

1. Enter your pseudocode in the text area
2. Adjust generation parameters in the sidebar (optional)
3. Click "Generate Python Code" button
4. Copy the generated code using the copy button

## Example Pseudocode Inputs

- `create integer variable x`
- `read input from user`
- `if x greater than 5 print yes`
- `for i from 0 to 10 print i`
- `create list numbers`

## Model Information

- **Base Model**: GPT-2 Small
- **Training Dataset**: SPOC (Pseudocode to Code)
- **Task**: Pseudocode → Python Code Generation
- **Architecture**: GPT2LMHeadModel (12 layers, 768 hidden size)

## Requirements

- Python 3.8+
- PyTorch
- Transformers library
- Streamlit

## Deployment to Streamlit Cloud

### Step 1: Prepare Your Repository
1. Upload all your files to a GitHub repository:
   - `app.py`
   - `requirements.txt`
   - All model files (`model.safetensors`, `config.json`, `tokenizer_config.json`, `vocab.json`, `merges.txt`, `special_tokens_map.json`)
   - `.streamlit/config.toml` (optional, for custom theming)

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository and branch
5. Set the main file path to: `app.py`
6. Click "Deploy"

### Important Notes for Streamlit Cloud:
- **Model Size**: If your model files are large (>100MB), consider using Git LFS or hosting them on cloud storage (S3, Google Drive, etc.) and downloading them at runtime
- **Memory Limits**: Streamlit Cloud has memory limits, so ensure your model fits within the constraints
- **Startup Time**: First load may take a few minutes as Streamlit Cloud installs dependencies and loads your model
- **CPU Only**: Streamlit Cloud runs on CPU, so GPU optimizations won't apply

### Alternative: Using Cloud Storage for Large Models
If your model is too large for GitHub, modify `app.py` to download from cloud storage:

```python
# Add this to load_model() function if needed
import requests

def download_model_from_url(url, local_path):
    response = requests.get(url, stream=True)
    with open(local_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
```

## Local Development

If you want to test locally before deploying:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## Notes

- The model automatically uses GPU if CUDA is available (local only; Streamlit Cloud uses CPU)
- Generation parameters can be adjusted in the sidebar for different outputs
- The model expects pseudocode in natural language format

