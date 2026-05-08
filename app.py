import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
import json
import time
import re

# 1️⃣ Streamlit page configuration
st.set_page_config(
    page_title="CodeSense AI 💻",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2️⃣ Custom CSS Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    
    .main > div {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    .codesense-title { text-align: center; margin-bottom: 30px; }
    
    .codesense-title h1 {
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        margin-bottom: 10px !important;
        background: linear-gradient(135deg, #2d1b4e 0%, #4a2c6d 50%, #667eea 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        display: inline-block !important;
        animation: float 3s ease-in-out infinite !important;
    }
    
    .codesense-title p { font-size: 1.1rem !important; font-weight: 500 !important; color: #4a2c6d !important; }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    [data-testid="stSidebar"] > div:first-child { padding: 0.8rem 0.8rem !important; }
    
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] label { color: #ffffff !important; }
    
    .sidebar-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 10px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 15px;
    }
    
    .sidebar-title h2 { color: white !important; margin: 0 !important; font-size: 18px !important; }
    [data-testid="stSidebar"] h3 { color: #ffffff !important; margin: 8px 0 5px 0 !important; font-size: 14px !important; }
    [data-testid="stSidebar"] hr { margin: 8px 0 !important; border-color: rgba(255,255,255,0.15) !important; }
    [data-testid="stSidebar"] strong { color: #ffffff !important; font-size: 12px !important; margin: 5px 0 3px 0 !important; display: block !important; }
    
    [data-testid="stSidebar"] .stSelectbox {
        margin: 5px 0 10px 0 !important;
        width: 100% !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
        min-height: 42px !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] span {
        color: white !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        white-space: normal !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox svg { fill: white !important; stroke: white !important; }
    [data-testid="stSidebar"] .stSelectbox ul { background: #1a1a2e !important; }
    [data-testid="stSidebar"] .stSelectbox li { color: white !important; padding: 10px 12px !important; }
    [data-testid="stSidebar"] .stSelectbox li:hover { background: #667eea !important; }
    [data-testid="stSidebar"] .stSelectbox li[aria-selected="true"] { background: #667eea !important; font-weight: bold !important; }
    
    [data-testid="stSidebar"] div.stButton { margin: 10px 0 !important; width: 100% !important; }
    [data-testid="stSidebar"] div.stButton > button {
        background: linear-gradient(135deg, #00b4db 0%, #0083b0 100%) !important;
        color: white !important;
        font-weight: 900 !important;
        font-size: 14px !important;
        padding: 10px 16px !important;
        width: 100% !important;
        border-radius: 10px !important;
    }
    
    .features-card {
        background: linear-gradient(135deg, rgba(102,126,234,0.15) 0%, rgba(118,75,162,0.15) 100%);
        border-radius: 10px;
        padding: 10px !important;
        margin: 15px 0 !important;
    }
    .features-card h3 { margin: 0 0 8px 0 !important; font-size: 14px !important; text-align: center !important; color: #fff !important; }
    .feature-item { display: flex !important; align-items: center !important; padding: 4px 8px !important; margin: 3px 0 !important; background: rgba(255,255,255,0.08); border-radius: 6px; }
    .feature-item:hover { background: rgba(102,126,234,0.3); transform: translateX(3px); }
    .feature-icon { font-size: 14px !important; margin-right: 8px !important; }
    .feature-text { font-size: 11px !important; color: #fff !important; }
    
    .custom-card {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 8px !important;
        margin: 10px 0 !important;
        text-align: center;
    }
    .custom-card h3 { margin: 0 0 3px 0 !important; font-size: 13px !important; color: #fff !important; }
    .custom-card p { margin: 2px 0 !important; font-size: 10px !important; color: #ddd !important; }
    
    div.stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 50px !important;
        padding: 10px 30px !important;
        font-size: 16px !important;
    }
    
    textarea {
        background: #f8f9fa !important;
        border: 2px solid #667eea !important;
        border-radius: 15px !important;
        font-family: 'Courier New', monospace !important;
    }
    
    .result-box {
        background: linear-gradient(135deg, #e8f0ff 0%, #f0e8ff 100%);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 4px solid #667eea;
    }
    
    .correct-code-box {
        background: linear-gradient(135deg, #e8fff0 0%, #d4ffd4 100%);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 4px solid #00cc44;
    }
    
    .converted-code-box {
        background: linear-gradient(135deg, #e0f7ff 0%, #cceeff 100%);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 4px solid #00aaff;
    }
    
    .issues-box {
        background: linear-gradient(135deg, #ffe8f0 0%, #ffe0e8 100%);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 4px solid #ff6384;
    }
    
    .suggestions-box {
        background: linear-gradient(135deg, #e8fff0 0%, #e0ffe8 100%);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 4px solid #4bc0c0;
    }
    
    .explanation-box {
        background: linear-gradient(135deg, #fff8e8 0%, #fff0e0 100%);
        border-radius: 15px;
        padding: 15px;
        max-height: 400px;
        overflow-y: auto;
        border-left: 4px solid #ffce56;
    }
    
    .docs-box {
        background: linear-gradient(135deg, #f0e8ff 0%, #e8d8ff 100%);
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 15px;
        border-left: 4px solid #9b59b6;
        max-height: 600px;
        overflow-y: auto;
    }
    
    .docs-box h1, .docs-box h2, .docs-box h3 {
        color: #6c3483;
    }
    
    .docs-box code {
        background: #f0e8ff;
        padding: 2px 5px;
        border-radius: 4px;
    }
    
    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 30px;
        border-top: 2px solid rgba(0, 0, 0, 0.1);
    }
    .footer p { color: #1a1a2e !important; font-size: 1.2rem !important; font-weight: 900 !important; }
</style>
""", unsafe_allow_html=True)

# 3️⃣ Load API key
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    st.error("❌ GROQ_API_KEY not found in .env file!")
    st.info("Get your free API key from: https://console.groq.com")
    st.stop()

# 4️⃣ Create Groq client
client = Groq(api_key=API_KEY)

# 5️⃣ Build prompt based on mode
def build_prompt(user_code, mode, explanation_lang, target_lang=None):
    lang = "English" if explanation_lang == "English" else "Urdu"
    
    if mode == "Fix Bugs":
        return f"""Fix ALL bugs in this code. Return ONLY valid JSON.

CODE:
{user_code}

RETURN EXACT JSON:
{{"result": "summary", "corrected_code": "fixed code", "issues": ["issue1","issue2"], "suggestions": ["sug1","sug2"], "explanation": "explanation in {lang}"}}"""

    elif mode == "Optimize Code":
        return f"""Optimize this code. Return ONLY valid JSON.

CODE:
{user_code}

RETURN EXACT JSON:
{{"result": "summary", "corrected_code": "optimized code", "issues": ["issue1"], "suggestions": ["opt1","opt2"], "explanation": "explanation in {lang}"}}"""

    elif mode == "Explain Code":
        return f"""Explain this code in DETAIL. Return ONLY valid JSON.

CODE:
{user_code}

RETURN EXACT JSON:
{{"result": "summary", "corrected_code": "", "issues": [], "suggestions": [], "explanation": "detailed line by line explanation in {lang}"}}"""

    elif mode == "Generate Docs":
        return f"""Generate COMPREHENSIVE, DETAILED professional documentation for this code. Return ONLY valid JSON.

CODE:
{user_code}

REQUIREMENTS FOR DETAILED DOCUMENTATION:
1. Write at least 500-1000 words
2. Include ALL of these sections:
   - ## 📋 Overview / Purpose
   - ## 📦 Installation & Setup
   - ## 📚 Class/Function Description
   - ## 🔧 Parameters (each parameter with type, description)
   - ## 📤 Return Value
   - ## 🚀 Usage Examples (at least 3 examples)
   - ## ⚠️ Edge Cases & Error Handling
   - ## ⚡ Performance Considerations
   - ## 🔒 Security Notes
   - ## 📝 Code Walkthrough
   - ## 🎯 Best Practices
   - ## 📄 License Information

3. Use proper markdown formatting with ## headings, ``` code blocks, bullet points
4. Include real, working code examples with inputs and outputs

RETURN EXACT JSON:
{{"result": "brief summary", "corrected_code": "", "issues": [], "suggestions": [], "explanation": "COMPLETE DETAILED DOCUMENTATION HERE with ALL sections"}}"""

    elif mode == "Convert Code" and target_lang:
        return f"""Convert this code to {target_lang}. Return ONLY valid JSON.

CODE:
{user_code}
TARGET: {target_lang}

RETURN EXACT JSON:
{{"result": "summary", "corrected_code": "converted code in {target_lang}", "issues": [], "suggestions": [], "explanation": "explanation in {lang}"}}"""

    return ""

# 6️⃣ Typing effect
def type_text(text):
    placeholder = st.empty()
    typed = ""
    for char in text:
        typed += char
        placeholder.markdown(f'<div class="explanation-box">{typed}</div>', unsafe_allow_html=True)
        time.sleep(0.005)

# 7️⃣ Call Groq AI
def call_groq(prompt_text):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are CodeSense. Return ONLY valid JSON. No markdown, no extra text. Make documentation VERY DETAILED with multiple sections."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.3,
            max_tokens=4096
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

# 8️⃣ Safe JSON extraction
def safe_parse_json(text):
    if not text:
        return None
    
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    
    start = text.find('{')
    end = text.rfind('}')
    
    if start == -1 or end == -1:
        return None
    
    json_str = text[start:end+1]
    json_str = re.sub(r',\s*}', '}', json_str)
    json_str = re.sub(r',\s*]', ']', json_str)
    
    try:
        return json.loads(json_str)
    except:
        return None

# 9️⃣ Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-title"><h2>✨ CodeSense AI</h2></div>', unsafe_allow_html=True)
    st.markdown("### ⚙️ Settings")
    st.markdown("---")
    
    st.markdown("**Select Task Mode**")
    mode = st.selectbox("", ["Fix Bugs", "Optimize Code", "Explain Code", "Generate Docs", "Convert Code"], label_visibility="collapsed")
    st.markdown("---")
    
    st.markdown("**Explanation Language**")
    explanation_lang = st.selectbox("", ["English", "Urdu"], label_visibility="collapsed")
    
    target_lang = None
    if mode == "Convert Code":
        st.markdown("---")
        st.markdown("**Target Language**")
        target_lang = st.selectbox("", ["Python", "JavaScript", "Java", "C++", "C#", "Go", "TypeScript"], label_visibility="collapsed")
    
    st.markdown("---")
    
    st.markdown("""
    <div class="features-card">
        <h3>🎯 Key Features</h3>
        <div class="feature-item"><span class="feature-icon">🐞</span><span class="feature-text">Fix Bugs + Code</span></div>
        <div class="feature-item"><span class="feature-icon">⚡</span><span class="feature-text">Optimize + Code</span></div>
        <div class="feature-item"><span class="feature-icon">📖</span><span class="feature-text">Explain Code</span></div>
        <div class="feature-item"><span class="feature-icon">📄</span><span class="feature-text">Documentation (Detailed)</span></div>
        <div class="feature-item"><span class="feature-icon">🔄</span><span class="feature-text">Convert Code</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    run_btn = st.button("🚀 Run Analysis", type="primary", use_container_width=True)
    st.markdown("---")
    
    st.markdown("""
    <div class="custom-card">
        <h3>📊 Stats</h3>
        <p>🤖 Free AI (Groq)</p>
        <p>⚡ Fast Response</p>
        <p>✅ All 5 Modes Working</p>
        <p>📚 Detailed Documentation</p>
    </div>
    """, unsafe_allow_html=True)

# 🔟 Main UI
st.markdown('<div class="codesense-title"><h1>💻 CodeSense AI</h1><p>Your Intelligent Code Assistant</p></div>', unsafe_allow_html=True)
st.markdown("---")
st.markdown("### 📝 Input Code")
code = st.text_area("", height=350, placeholder="# Paste your code here...", label_visibility="collapsed")

if not run_btn:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        run_btn = st.button("✨ Run AI Analysis ✨", type="primary", use_container_width=True)

if run_btn:
    if not code.strip():
        st.warning("⚠️ Please enter some code!")
    else:
        prompt_text = build_prompt(code, mode, explanation_lang, target_lang)
        
        messages = {
            "Fix Bugs": "🐞 Finding and fixing bugs...",
            "Optimize Code": "⚡ Optimizing your code...",
            "Explain Code": "📖 Analyzing and explaining...",
            "Generate Docs": "📄 Generating detailed documentation...",
            "Convert Code": f"🔄 Converting to {target_lang}..."
        }
        
        with st.spinner(messages.get(mode, "🤖 AI is thinking...")):
            raw_output = call_groq(prompt_text)
        
        data = safe_parse_json(raw_output)
        
        if not data:
            st.error("❌ Could not parse response. Please try again.")
            with st.expander("Raw Response"):
                st.code(raw_output[:1000] if raw_output else "No response")
            st.stop()
        
        try:
            if "import" in code or "def " in code:
                lang = "python"
            elif "#include" in code:
                lang = "cpp"
            elif "function" in code or "console.log" in code:
                lang = "javascript"
            else:
                lang = "text"
            
            st.markdown("## 📊 Analysis Results")
            
            if data.get("result"):
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown("### 📋 Summary")
                st.write(data["result"])
                st.markdown('</div>', unsafe_allow_html=True)
            
            if mode in ["Fix Bugs", "Optimize Code"] and data.get("corrected_code") and data["corrected_code"].strip():
                box_title = "### 🔧 Fixed Code" if mode == "Fix Bugs" else "### ⚡ Optimized Code"
                st.markdown('<div class="correct-code-box">', unsafe_allow_html=True)
                st.markdown(box_title)
                st.code(data["corrected_code"], language=lang)
                st.markdown('</div>', unsafe_allow_html=True)
            
            elif mode == "Convert Code" and data.get("corrected_code") and data["corrected_code"].strip():
                st.markdown('<div class="converted-code-box">', unsafe_allow_html=True)
                st.markdown(f"### 🔄 Converted Code ({target_lang})")
                output_lang = target_lang.lower() if target_lang else "text"
                st.code(data["corrected_code"], language=output_lang)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Documentation - Now with scrollable box for long content
            if mode == "Generate Docs" and data.get("explanation"):
                st.markdown('<div class="docs-box">', unsafe_allow_html=True)
                st.markdown("### 📚 Detailed Documentation")
                st.markdown(data["explanation"])
                st.markdown('</div>', unsafe_allow_html=True)
            
            if data.get("issues") and len(data["issues"]) > 0 and data["issues"][0]:
                st.markdown('<div class="issues-box">', unsafe_allow_html=True)
                title = "### ⚠️ Issues Found" if mode == "Fix Bugs" else "### ⚠️ Notes"
                st.markdown(title)
                for issue in data["issues"]:
                    if issue and issue.strip():
                        st.markdown(f"• {issue}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            if data.get("suggestions") and len(data["suggestions"]) > 0 and data["suggestions"][0]:
                st.markdown('<div class="suggestions-box">', unsafe_allow_html=True)
                title = "### 💡 Optimization Tips" if mode == "Optimize Code" else "### 💡 Suggestions"
                st.markdown(title)
                for sug in data["suggestions"]:
                    if sug and sug.strip():
                        st.markdown(f"• {sug}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            if mode != "Generate Docs" and data.get("explanation"):
                st.markdown('<div class="explanation-box">', unsafe_allow_html=True)
                if mode == "Explain Code":
                    st.markdown(f"### 📘 Code Explanation ({explanation_lang})")
                elif mode == "Fix Bugs":
                    st.markdown(f"### 📘 Fix Explanation ({explanation_lang})")
                elif mode == "Optimize Code":
                    st.markdown(f"### 📘 Optimization Explanation ({explanation_lang})")
                elif mode == "Convert Code":
                    st.markdown(f"### 📘 Conversion Explanation ({explanation_lang})")
                type_text(data["explanation"])
                st.markdown('</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Footer
st.markdown('<div class="footer"><p>✨ CodeSense AI - Intelligent Coding Assistant ✨</p></div>', unsafe_allow_html=True)