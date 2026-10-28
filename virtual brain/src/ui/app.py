"""
Streamlit UI for RAJIV - Modern Premium Design
"""

import streamlit as st
import sys
import os
from pathlib import Path
from datetime import datetime
import time

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.config_manager import ConfigurationManager
from src.input.input_module import InputModule
from src.ai_core.ai_core import AICore
from src.memory.memory_system import MemorySystem
from src.tasks.task_executor import TaskExecutor
from src.output.output_module import OutputModule
from src.jarvis.jarvis_core import JARVISCore


def initialize_components():
    config_manager = ConfigurationManager()
    memory_system = MemorySystem(
        embedding_model=config_manager.get('memory.embedding_model'),
        dimension=384
    )
    task_executor = TaskExecutor()
    jarvis_core = JARVISCore()
    llm_settings = config_manager.get_llm_settings()
    ai_core = AICore(
        llm_config=llm_settings,
        memory_system=memory_system,
        task_executor=task_executor
    )
    voice_settings = config_manager.get_voice_settings()
    input_module = InputModule()
    output_module = OutputModule(voice_enabled=voice_settings.get('output_enabled', True))
    return config_manager, input_module, ai_core, output_module, jarvis_core


def initialize_session_state():
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'components_initialized' not in st.session_state:
        st.session_state.components_initialized = False
    if 'voice_output_enabled' not in st.session_state:
        st.session_state.voice_output_enabled = True
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'show_recent' not in st.session_state:
        st.session_state.show_recent = False
    # current session messages (only this session)
    if 'current_messages' not in st.session_state:
        st.session_state.current_messages = []
    if 'voice_triggered' not in st.session_state:
        st.session_state.voice_triggered = False
    if 'voice_status' not in st.session_state:
        st.session_state.voice_status = ""


def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* ═══════════════════════════════════════════════════════════
       GLOBAL STYLES - Modern Dark Theme with Gradient
    ═══════════════════════════════════════════════════════════ */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%) !important;
        color: #ffffff !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }
    
    /* ═══════════════════════════════════════════════════════════
       SIDEBAR - Glassmorphism Effect
    ═══════════════════════════════════════════════════════════ */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] h3 {
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* ═══════════════════════════════════════════════════════════
       HEADER - Premium Animated Header
    ═══════════════════════════════════════════════════════════ */
    .rajiv-header {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 30px;
        display: flex;
        align-items: center;
        gap: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        animation: fadeInDown 0.6s ease-out;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .rajiv-icon {
        font-size: 3.5rem;
        animation: pulse 2s ease-in-out infinite;
        filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.6));
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .rajiv-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 3px;
        margin: 0;
        line-height: 1.2;
    }
    
    .rajiv-subtitle {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 400;
        margin-top: 5px;
        letter-spacing: 1px;
    }
    
    .status-badge {
        display: inline-block;
        background: rgba(76, 175, 80, 0.2);
        color: #4caf50;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid rgba(76, 175, 80, 0.3);
        margin-top: 10px;
    }
    
    .status-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        background: #4caf50;
        border-radius: 50%;
        margin-right: 8px;
        animation: blink 1.5s ease-in-out infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    
    /* ═══════════════════════════════════════════════════════════
       CHAT BUBBLES - Modern Message Design
    ═══════════════════════════════════════════════════════════ */
    .msg-row-user {
        display: flex;
        justify-content: flex-end;
        margin: 16px 0;
        animation: slideInRight 0.3s ease-out;
    }
    
    .msg-row-bot {
        display: flex;
        justify-content: flex-start;
        margin: 16px 0;
        animation: slideInLeft 0.3s ease-out;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .bubble-user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        padding: 14px 20px;
        border-radius: 20px 20px 4px 20px;
        max-width: 70%;
        font-size: 0.95rem;
        line-height: 1.6;
        white-space: pre-wrap;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        font-weight: 500;
    }
    
    .bubble-bot {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        color: #ffffff;
        padding: 14px 20px;
        border-radius: 20px 20px 20px 4px;
        max-width: 70%;
        font-size: 0.95rem;
        line-height: 1.6;
        white-space: pre-wrap;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        font-weight: 400;
    }
    
    .msg-time {
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.5);
        margin-top: 6px;
        font-weight: 400;
    }
    
    /* ═══════════════════════════════════════════════════════════
       INPUT & BUTTONS - Premium Interactive Elements
    ═══════════════════════════════════════════════════════════ */
    [data-testid="stTextInput"] input {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px) !important;
        color: #000000 !important;
        border: 1.5px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
        padding: 14px 20px !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        -webkit-text-fill-color: #000000 !important;
    }
    
    [data-testid="stTextInput"] input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.3) !important;
        background: rgba(255, 255, 255, 1) !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
    
    [data-testid="stTextInput"] input::placeholder {
        color: rgba(0, 0, 0, 0.4) !important;
        -webkit-text-fill-color: rgba(0, 0, 0, 0.4) !important;
    }
    
    /* Force text visibility in all states */
    [data-testid="stTextInput"] input:-webkit-autofill,
    [data-testid="stTextInput"] input:-webkit-autofill:hover,
    [data-testid="stTextInput"] input:-webkit-autofill:focus {
        -webkit-text-fill-color: #000000 !important;
        -webkit-box-shadow: 0 0 0px 1000px rgba(255, 255, 255, 0.95) inset !important;
        transition: background-color 5000s ease-in-out 0s !important;
    }
    
    /* Buttons - Gradient Style */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        font-size: 0.95rem !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    .stButton > button:disabled {
        background: rgba(255, 255, 255, 0.1) !important;
        color: rgba(255, 255, 255, 0.3) !important;
        box-shadow: none !important;
    }
    
    /* Form Submit Button */
    [data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        width: 100% !important;
        padding: 12px !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Toggle Switch */
    [data-testid="stToggle"] {
        accent-color: #667eea !important;
    }
    
    /* ═══════════════════════════════════════════════════════════
       PANELS & CARDS - Glassmorphism Design
    ═══════════════════════════════════════════════════════════ */
    .recent-panel {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        margin-top: 15px;
        max-height: 450px;
        overflow-y: auto;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .recent-item {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 12px;
        transition: all 0.3s ease;
    }
    
    .recent-item:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateX(5px);
    }
    
    .recent-item:last-child {
        margin-bottom: 0;
    }
    
    .recent-q {
        font-weight: 600;
        color: #667eea;
        font-size: 0.9rem;
        margin-bottom: 6px;
    }
    
    .recent-a {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.85rem;
        line-height: 1.5;
    }
    
    .recent-t {
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.4);
        margin-top: 8px;
    }
    
    /* ═══════════════════════════════════════════════════════════
       EMPTY STATE - Welcoming Design
    ═══════════════════════════════════════════════════════════ */
    .empty-chat {
        text-align: center;
        padding: 80px 20px;
        animation: fadeIn 0.8s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .empty-chat .icon {
        font-size: 5rem;
        margin-bottom: 20px;
        filter: drop-shadow(0 0 30px rgba(102, 126, 234, 0.5));
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .empty-chat .title {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 12px;
    }
    
    .empty-chat .subtitle {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.6);
        font-weight: 400;
        line-height: 1.6;
    }
    
    .suggestion-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: center;
        margin-top: 30px;
    }
    
    .chip {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 10px 20px;
        border-radius: 25px;
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.8);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .chip:hover {
        background: rgba(102, 126, 234, 0.2);
        border-color: #667eea;
        transform: translateY(-2px);
    }
    
    /* ═══════════════════════════════════════════════════════════
       METRICS & INFO CARDS
    ═══════════════════════════════════════════════════════════ */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px;
    }
    
    /* Divider */
    hr {
        border-color: rgba(255, 255, 255, 0.1) !important;
        margin: 20px 0 !important;
    }
    
    /* Info/Warning/Error boxes */
    .stAlert {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(102, 126, 234, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(102, 126, 234, 0.7);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    </style>
    """, unsafe_allow_html=True)


def render_chat_bubble(role: str, text: str, timestamp: str = ""):
    if role == "user":
        st.markdown(f"""
        <div class="msg-row-user">
            <div>
                <div class="bubble-user">{text}</div>
                <div class="msg-time">{timestamp}</div>
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="msg-row-bot">
            <div>
                <div class="bubble-bot">{text}</div>
                <div class="msg-time">{timestamp}</div>
            </div>
        </div>""", unsafe_allow_html=True)


def process_user_input(user_input: str, ai_core: AICore, output_module: OutputModule):
    if not user_input or not user_input.strip():
        return

    try:
        st.session_state.processing = True
        jarvis_core = st.session_state.jarvis_core
        jarvis_result = jarvis_core.process_jarvis_command(user_input)

        if jarvis_result['success']:
            response = jarvis_result['message']
        else:
            with st.spinner("BEST is thinking..."):
                response = ai_core.process_command(user_input)

        output_module.output_response(response, use_voice=st.session_state.voice_output_enabled)

        timestamp = datetime.now().strftime("%H:%M")
        entry = {'user': user_input, 'assistant': response, 'timestamp': timestamp}

        st.session_state.current_messages.append(entry)
        st.session_state.conversation_history.append(entry)
        st.session_state.processing = False
        st.rerun()

    except Exception as e:
        import traceback
        st.error(f"BEST encountered an error: {str(e)}")
        with st.expander("Error Details"):
            st.code(traceback.format_exc())
        st.session_state.processing = False


def main():
    st.set_page_config(
        page_title="BEST Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    initialize_session_state()
    apply_styles()

    # ── Sidebar ──────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### ⚙️ Settings")

        voice_enabled = st.toggle("🔊 Voice Output", value=st.session_state.voice_output_enabled)
        if voice_enabled != st.session_state.voice_output_enabled:
            st.session_state.voice_output_enabled = voice_enabled
            if st.session_state.components_initialized:
                st.session_state.output_module.set_voice_enabled(voice_enabled)

        st.divider()

        if st.session_state.components_initialized:
            st.markdown("### 🤖 AI Info")
            llm_provider = st.session_state.config_manager.get('llm.provider', 'Unknown')
            llm_model = st.session_state.config_manager.get('llm.model', 'Unknown')
            st.caption(f"**Provider:** {llm_provider}")
            st.caption(f"**Model:** {llm_model}")

            st.divider()

            if st.button("📊 System Status", use_container_width=True):
                process_user_input("system status", st.session_state.ai_core, st.session_state.output_module)

            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.current_messages = []
                st.session_state.conversation_history = []
                st.session_state.ai_core.clear_conversation_memory()
                st.rerun()

    # ── Initialize components ─────────────────────────────────
    if not st.session_state.components_initialized:
        with st.spinner("Starting BEST..."):
            try:
                config_manager, input_module, ai_core, output_module, jarvis_core = initialize_components()
                st.session_state.config_manager = config_manager
                st.session_state.input_module = input_module
                st.session_state.ai_core = ai_core
                st.session_state.output_module = output_module
                st.session_state.jarvis_core = jarvis_core
                st.session_state.components_initialized = True
                st.rerun()
            except Exception as e:
                st.error(f"Failed to start BEST: {str(e)}")
                st.stop()

    # ── Header ───────────────────────────────────────────────
    st.markdown("""
    <div class="rajiv-header">
        <span class="rajiv-icon">🤖</span>
        <div style="flex: 1;">
            <div class="rajiv-title">BEST</div>
            <div class="rajiv-subtitle">Intelligent Virtual Assistant • Powered by AI</div>
            <div class="status-badge">
                <span class="status-dot"></span>Online & Ready
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Top action bar ────────────────────────────────────────
    col_btn1, col_btn2, col_btn3, col_spacer = st.columns([1, 1, 1, 5])

    with col_btn1:
        if st.button("🕘 Recent Chats"):
            st.session_state.show_recent = not st.session_state.show_recent

    with col_btn2:
        mic_disabled = not st.session_state.input_module.microphone_available
        voice_btn = st.button("🎤 Voice", disabled=mic_disabled)

    with col_btn3:
        if st.button("🗑️ Clear"):
            st.session_state.current_messages = []
            st.session_state.ai_core.clear_conversation_memory()
            st.rerun()

    # ── Recent Chats Panel ────────────────────────────────────
    if st.session_state.show_recent:
        history = st.session_state.conversation_history
        if not history:
            st.info("No chat history yet.")
        else:
            st.markdown('<div class="recent-panel">', unsafe_allow_html=True)
            st.markdown(f"**Recent Chats** ({len(history)} messages)")
            for entry in reversed(history[-20:]):
                q = entry.get('user', '')
                a = entry.get('assistant', '')
                t = entry.get('timestamp', '')
                a_short = (a[:120] + "…") if len(a) > 120 else a
                st.markdown(f"""
                <div class="recent-item">
                    <div class="recent-q">You: {q}</div>
                    <div class="recent-a">BEST: {a_short}</div>
                    <div class="recent-t">{t}</div>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.divider()

    # ── Input Form ────────────────────────────────────────────
    with st.form(key="chat_form", clear_on_submit=True):
        col_input, col_send, col_voice_toggle = st.columns([7, 1, 1])
        with col_input:
            user_text = st.text_input(
                label="message",
                placeholder="Ask BEST anything...",
                label_visibility="collapsed"
            )
        with col_send:
            submitted = st.form_submit_button("Send")
        with col_voice_toggle:
            # Speaker toggle inside the form row
            spk = st.form_submit_button(
                "🔊 ON" if st.session_state.voice_output_enabled else "🔇 OFF"
            )

    if submitted and user_text and user_text.strip():
        process_user_input(user_text, st.session_state.ai_core, st.session_state.output_module)

    # Toggle speaker if that button was clicked
    if spk:
        st.session_state.voice_output_enabled = not st.session_state.voice_output_enabled
        if st.session_state.components_initialized:
            st.session_state.output_module.set_voice_enabled(
                st.session_state.voice_output_enabled
            )
        st.rerun()

    # ── Handle voice — capture BEFORE chat renders ────────────
    if voice_btn:
        if not st.session_state.input_module.microphone_available:
            st.session_state.voice_status = "error:Microphone not available."
        else:
            status_placeholder = st.empty()
            status_placeholder.info("🎤 Listening... speak now!")
            try:
                voice_text = st.session_state.input_module.capture_voice_input(
                    timeout=10, phrase_time_limit=15
                )
                status_placeholder.empty()
                st.session_state.voice_status = ""
                # Process immediately — result will appear below input bar
                process_user_input(
                    voice_text,
                    st.session_state.ai_core,
                    st.session_state.output_module
                )
            except Exception as e:
                status_placeholder.empty()
                st.session_state.voice_status = f"error:{str(e)}"
                st.rerun()

    # Show any persistent voice status message
    if st.session_state.voice_status:
        if st.session_state.voice_status.startswith("error:"):
            st.error(f"❌ {st.session_state.voice_status[6:]}")
        else:
            st.info(st.session_state.voice_status)

    # ── Current Chat Area (always below input) ────────────────
    if not st.session_state.current_messages:
        st.markdown("""
        <div class="empty-chat">
            <div class="icon">💬</div>
            <div class="title">Welcome to BEST</div>
            <div class="subtitle">
                Your intelligent virtual assistant is ready to help.<br>
                Ask me anything - from system tasks to general questions.
            </div>
        </div>""", unsafe_allow_html=True)
        
        # Suggestion buttons
        st.markdown("### Quick Actions")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📊 System Status", key="sys_status", use_container_width=True):
                process_user_input("system status", st.session_state.ai_core, st.session_state.output_module)
        
        with col2:
            if st.button("📁 Organize Files", key="organize", use_container_width=True):
                process_user_input("organize desktop", st.session_state.ai_core, st.session_state.output_module)
        
        with col3:
            if st.button("🕐 What time is it?", key="time", use_container_width=True):
                process_user_input("what time is it?", st.session_state.ai_core, st.session_state.output_module)
        
        with col4:
            if st.button("🧮 Calculate 25 * 48", key="calc", use_container_width=True):
                process_user_input("calculate 25 * 48", st.session_state.ai_core, st.session_state.output_module)
    else:
        # Newest message at top, oldest at bottom
        for entry in reversed(st.session_state.current_messages):
            render_chat_bubble("user", entry['user'], entry['timestamp'])
            render_chat_bubble("bot", entry['assistant'], entry['timestamp'])


if __name__ == "__main__":
    main()
