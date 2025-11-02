import streamlit as st
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Pseudocode to Python Generator",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        padding-bottom: 2rem;
    }
    .code-block {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'model' not in st.session_state:
    st.session_state.model = None
if 'tokenizer' not in st.session_state:
    st.session_state.tokenizer = None
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False

@st.cache_resource
def load_model():
    """Load the fine-tuned GPT-2 model and tokenizer"""
    try:
        # Get the directory where the model files are located
        model_dir = Path(".")
        
        # Check if model files exist
        if not (model_dir / "model.safetensors").exists() and not (model_dir / "pytorch_model.bin").exists():
            st.error("❌ Model file not found! Please ensure model.safetensors is in the same directory as app.py")
            return None, None
        
        # Load tokenizer
        tokenizer = GPT2Tokenizer.from_pretrained(model_dir)
        tokenizer.pad_token = tokenizer.eos_token
        
        # Load model
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = GPT2LMHeadModel.from_pretrained(model_dir)
        model.to(device)
        model.eval()
        
        return model, tokenizer
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        return None, None

def generate_code(pseudocode, model, tokenizer, max_length=150, temperature=0.7, top_p=0.9):
    """Generate Python code from pseudocode"""
    try:
        # Format prompt as the model was trained
        prompt = f"### PSEUDOCODE:\n{pseudocode}\n### PYTHON CODE:\n"
        
        # Tokenize input
        device = "cuda" if torch.cuda.is_available() else "cpu"
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        
        # Generate code
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
                repetition_penalty=1.2,
                no_repeat_ngram_size=3
            )
        
        # Decode generated text
        generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract Python code from generated text
        if "### PYTHON CODE:" in generated:
            code = generated.split("### PYTHON CODE:")[1].strip()
            # Remove any trailing PSEUDOCODE markers if present
            if "### PSEUDOCODE:" in code:
                code = code.split("### PSEUDOCODE:")[0].strip()
            return code
        else:
            # If format doesn't match, return the generated text after the prompt
            if prompt in generated:
                return generated.split(prompt)[1].strip()
            return generated
            
    except Exception as e:
        return f"Error generating code: {str(e)}"

# Main UI
st.markdown('<p class="main-header">🐍 Pseudocode to Python Generator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Fine-tuned GPT-2 Model for Converting Pseudocode to Python Code</p>', unsafe_allow_html=True)

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    st.subheader("Generation Parameters")
    max_length = st.slider("Max Length", min_value=50, max_value=300, value=150, step=10)
    temperature = st.slider("Temperature", min_value=0.1, max_value=2.0, value=0.7, step=0.1)
    top_p = st.slider("Top-p (Nucleus)", min_value=0.1, max_value=1.0, value=0.9, step=0.05)
    
    st.markdown("---")
    st.subheader("ℹ️ About")
    st.info("""
    This app uses a fine-tuned GPT-2 model 
    trained on the SPOC dataset to convert 
    pseudocode instructions to Python code.
    
    **Model**: GPT-2 Small
    **Task**: Pseudocode → Python Code
    """)
    
    st.markdown("---")
    if st.button("🔄 Reload Model"):
        st.cache_resource.clear()
        st.session_state.model = None
        st.session_state.tokenizer = None
        st.session_state.model_loaded = False
        st.rerun()

# Load model
if not st.session_state.model_loaded:
    with st.spinner("🔄 Loading model... This may take a moment."):
        model, tokenizer = load_model()
        if model is not None and tokenizer is not None:
            st.session_state.model = model
            st.session_state.tokenizer = tokenizer
            st.session_state.model_loaded = True
            st.success("✅ Model loaded successfully!")
        else:
            st.error("❌ Failed to load model. Please check if model files are present.")
            st.stop()

# Main input area
st.header("📝 Enter Pseudocode")

# Initialize example in session state
if 'example_text' not in st.session_state:
    st.session_state.example_text = ''

# Example pseudocode suggestions
st.markdown("**Quick Examples:**")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Example 1", key="ex1"):
        st.session_state.example_text = "create integer variable x"
        st.rerun()
with col2:
    if st.button("Example 2", key="ex2"):
        st.session_state.example_text = "read input from user"
        st.rerun()
with col3:
    if st.button("Example 3", key="ex3"):
        st.session_state.example_text = "if x greater than 5 print yes"
        st.rerun()
with col4:
    if st.button("Example 4", key="ex4"):
        st.session_state.example_text = "for i from 0 to 10 print i"
        st.rerun()

# Text input
pseudocode_input = st.text_area(
    "Enter your pseudocode:",
    value=st.session_state.example_text,
    height=150,
    placeholder="Example: create integer n\nread n\nprint n",
    key="pseudocode_input"
)

# Generate button
if st.button("🚀 Generate Python Code", type="primary"):
    if pseudocode_input.strip():
        with st.spinner("🤖 Generating Python code..."):
            generated_code = generate_code(
                pseudocode_input,
                st.session_state.model,
                st.session_state.tokenizer,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p
            )
            
            st.markdown("---")
            st.header("✨ Generated Python Code")
            
            # Display generated code with copy button
            st.code(generated_code, language="python")
            
            # Info about the generation
            device_info = "GPU (CUDA)" if torch.cuda.is_available() else "CPU"
            st.caption(f"💡 Tip: Click on the code block above to select and copy it | ⚡ Running on: {device_info}")
    else:
        st.warning("⚠️ Please enter some pseudocode before generating!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>Built with ❤️ using Streamlit and Transformers</p>
</div>
""", unsafe_allow_html=True)

