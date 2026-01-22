# import streamlit as st
# import os
# import time
# import warnings
# from logic import SurakshaBrain
# from styles import apply_custom_styles
# from gtts import gTTS
# from io import BytesIO

# # --- SETUP ---
# warnings.filterwarnings("ignore")
# st.set_page_config(page_title="SurakshaConnect PoC", page_icon="🛡️", layout="wide")

# # ==========================================
# # PASTE YOUR KEYS HERE
# # ==========================================
# GEMINI_KEY = "AIzaSyBhKFq8HAmtsLzTbaijNA9bQksFXQPy6JQ"
# DEEPGRAM_KEY = "0d1a4eeb2aa059e5cbfdff8f4b20cc584b0ca2ce"
# PINECONE_KEY = "pcsk_33Qwd9_4tAV4eLWQoeyX2WHKWSNPk816ApLbLY9LfJJwVzMQdLPxPKPJbKw7BafcRnoRMw"
# INDEX_NAME = "suraksha-index"

# # Session State
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "ivr_history" not in st.session_state:
#     st.session_state.ivr_history = []

# try:
#     brain = SurakshaBrain(GEMINI_KEY, DEEPGRAM_KEY, PINECONE_KEY, INDEX_NAME)
# except Exception as e:
#     st.error(f"Init Error: {e}")
#     st.stop()

# # APPLY STYLES
# apply_custom_styles()

# with st.sidebar:
#     st.title("📱 Device Simulation")
#     mode = st.radio("Select User Device:", ["Smartphone (WhatsApp)", "Feature Phone (IVR)"])
#     st.divider()
#     if st.button("🗑️ Clear Chat History"):
#         st.session_state.chat_history = []
#         st.session_state.ivr_history = []
#         st.rerun()
#     log_box = st.empty()

# st.title("🛡️ SurakshaConnect")

# # ==========================================
# # MODE 1: WHATSAPP (Smartphone)
# # ==========================================
# if mode == "Smartphone (WhatsApp)":
    
#     col1, col2, col3 = st.columns([1, 2, 1])
    
#     with col2:
#         # --- HTML CONSTRUCTION (NO INDENTATION TO PREVENT BUGS) ---
#         # We build the string flat to avoid Markdown "Code Block" errors
#         html_code = ""
#         html_code += '<div class="whatsapp-wrapper">'
#         html_code += '<div class="whatsapp-header">'
#         html_code += '<div class="profile-pic">🛡️</div>'
#         html_code += '<div class="header-info">'
#         html_code += '<div class="header-name">SurakshaConnect <span class="verified-badge">✔</span></div>'
#         html_code += '<div class="header-status">Official Business Account</div>'
#         html_code += '</div></div>'
        
#         html_code += '<div class="wa-chat-window">'
        
#         # Static Greeting
#         html_code += '<div class="wa-bubble-bot">'
#         html_code += 'Hello! I am SurakshaConnect. Ask me about Crop, Health, or Life insurance.'
#         html_code += '<div class="msg-time">10:00 AM</div>'
#         html_code += '</div>'
        
#         # Loop Messages
#         for msg in st.session_state.chat_history:
#             if msg['role'] == "user":
#                 html_code += f'<div class="wa-bubble-user">{msg["content"]}</div>'
#             else:
#                 html_code += f'<div class="wa-bubble-bot">{msg["content"]}</div>'
        
#         html_code += '</div></div>'
#         # ---------------------------------------------------------

#         # Render the HTML
#         st.markdown(html_code, unsafe_allow_html=True)

#         # Input Area
#         user_input = st.chat_input("Type a message...")
        
#         if user_input:
#             st.session_state.chat_history.append({"role": "user", "content": user_input})
#             st.rerun()

#         if st.session_state.chat_history and st.session_state.chat_history[-1]['role'] == "user":
#             with st.spinner("Typing..."):
#                 last_query = st.session_state.chat_history[-1]['content']
#                 context, sources = brain.get_rag_context(last_query)
                
#                 # Call Logic (Pass "en" safely)
#                 response = brain.generate_response(last_query, context, "en")
                
#                 st.session_state.chat_history.append({"role": "assistant", "content": response})
#                 st.rerun()

# # ==========================================
# # MODE 2: FEATURE PHONE (IVR)
# # ==========================================
# else:
#     col1, col2 = st.columns([1, 2])
    
#     with col1:
#         st.markdown("""
#         <div class="phone-body">
#             <div class="screen-text">
#                 📶 IDEA 4G<br><br>
#                 <strong style="color: #fff; background: green; padding: 2px 5px;">ON CALL</strong><br>
#                 Suraksha Agent<br>
#                 00:42
#             </div>
#             <div class="keypad">
#                 <div class="key">1</div><div class="key">2</div><div class="key">3</div>
#                 <div class="key">4</div><div class="key">5</div><div class="key">6</div>
#                 <div class="key">7</div><div class="key">8</div><div class="key">9</div>
#                 <div class="key">*</div><div class="key">0</div><div class="key">#</div>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

#     with col2:
#         st.info("ℹ️ INSTRUCTIONS: Speak naturally. The AI will reply with VOICE.")

#         with st.container(height=300):
#             for msg in st.session_state.ivr_history:
#                 role_icon = "👤 Farmer" if msg['role'] == "user" else "🤖 Agent"
#                 st.markdown(f"**{role_icon}:** {msg['content']}")
#                 st.divider()

#         audio_val = st.audio_input("🔴 Press to Speak / Reply")
        
#         if audio_val:
#             with st.spinner("Processing..."):
#                 # Unpack tuple: text + lang
#                 text, lang_code = brain.transcribe_audio(audio_val.read())
                
#                 st.session_state.ivr_history.append({"role": "user", "content": text})
#                 log_box.success(f"Detected: {lang_code}")
                
#                 context, sources = brain.get_rag_context(text)
#                 response = brain.generate_response(text, context, lang_code)
#                 st.session_state.ivr_history.append({"role": "assistant", "content": response})
                
#                 try:
#                     tts = gTTS(text=response, lang=lang_code, slow=False)
#                     audio_fp = BytesIO()
#                     tts.write_to_fp(audio_fp)
#                     st.audio(audio_fp, format='audio/mp3', start_time=0)
#                 except:
#                     st.warning("Audio generation failed.")

#                 time.sleep(1)
#                 st.rerun()


import streamlit as st
import os
import time
import warnings
from logic import SurakshaBrain
from styles import apply_custom_styles
# Removed gTTS import as requested

# --- SETUP ---
warnings.filterwarnings("ignore")
st.set_page_config(page_title="SurakshaConnect PoC", page_icon="🛡️", layout="wide")

# ==========================================
# PASTE YOUR KEYS HERE
# ==========================================
GEMINI_KEY = "AIzaSyDTxRXlPKGvAZbU-1KhZT-gwMfxM2HY4v4"
DEEPGRAM_KEY = "0d1a4eeb2aa059e5cbfdff8f4b20cc584b0ca2ce"
PINECONE_KEY = "pcsk_33Qwd9_4tAV4eLWQoeyX2WHKWSNPk816ApLbLY9LfJJwVzMQdLPxPKPJbKw7BafcRnoRMw"
INDEX_NAME = "suraksha-index"

# Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "ivr_history" not in st.session_state:
    st.session_state.ivr_history = []
if "last_audio_id" not in st.session_state:
    st.session_state.last_audio_id = None

try:
    brain = SurakshaBrain(GEMINI_KEY, DEEPGRAM_KEY, PINECONE_KEY, INDEX_NAME)
except Exception as e:
    st.error(f"Init Error: {e}")
    st.stop()

# APPLY STYLES
apply_custom_styles()

with st.sidebar:
    st.title("📱 Device Simulation")
    mode = st.radio("Select User Device:", ["Smartphone (WhatsApp)", "Feature Phone (IVR)"])
    st.divider()
    # Clear History Button to reset demo
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.session_state.ivr_history = []
        st.session_state.last_audio_id = None
        st.rerun()
    log_box = st.empty()

st.title("🛡️ SurakshaConnect")

# ==========================================
# MODE 1: WHATSAPP (Smartphone)
# ==========================================
if mode == "Smartphone (WhatsApp)":
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # --- HTML CONSTRUCTION ---
        html_code = ""
        html_code += '<div class="whatsapp-wrapper">'
        html_code += '<div class="whatsapp-header">'
        html_code += '<div class="profile-pic">🛡️</div>'
        html_code += '<div class="header-info">'
        html_code += '<div class="header-name">SurakshaConnect <span class="verified-badge">✔</span></div>'
        html_code += '<div class="header-status">Official Business Account</div>'
        html_code += '</div></div>'
        
        html_code += '<div class="wa-chat-window">'
        
        # Static Greeting
        html_code += '<div class="wa-bubble-bot">'
        html_code += 'Hello! I am SurakshaConnect. Ask me about Crop, Health, or Life insurance.'
        html_code += '<div class="msg-time">10:00 AM</div>'
        html_code += '</div>'
        
        # Loop Messages
        for msg in st.session_state.chat_history:
            if msg['role'] == "user":
                html_code += f'<div class="wa-bubble-user">{msg["content"]}</div>'
            else:
                html_code += f'<div class="wa-bubble-bot">{msg["content"]}</div>'
        
        html_code += '</div></div>'
        # ---------------------------------------------------------

        # Render the HTML
        st.markdown(html_code, unsafe_allow_html=True)

        # Input Area
        user_input = st.chat_input("Type a message...")
        
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.rerun()

        if st.session_state.chat_history and st.session_state.chat_history[-1]['role'] == "user":
            with st.spinner("Typing..."):
                last_query = st.session_state.chat_history[-1]['content']
                context, sources = brain.get_rag_context(last_query)
                response = brain.generate_response(last_query, context)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()

# ==========================================
# MODE 2: FEATURE PHONE (IVR) - UPDATED
# ==========================================
else:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div class="phone-body">
            <div class="screen-text">
                📶 IDEA 4G<br><br>
                <strong style="color: #fff; background: green; padding: 2px 5px;">ON CALL</strong><br>
                Suraksha Agent<br>
                00:42
            </div>
            <div class="keypad">
                <div class="key">1</div><div class="key">2</div><div class="key">3</div>
                <div class="key">4</div><div class="key">5</div><div class="key">6</div>
                <div class="key">7</div><div class="key">8</div><div class="key">9</div>
                <div class="key">*</div><div class="key">0</div><div class="key">#</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.info("ℹ️ INSTRUCTIONS: Speak naturally. The AI will reply in TEXT (Simulating IVR menu).")

        # Chat Container
        with st.container(height=400):
            # Display History
            for msg in st.session_state.ivr_history:
                role_icon = "👤 Farmer" if msg['role'] == "user" else "🤖 Agent"
                st.markdown(f"**{role_icon}:** {msg['content']}")
                st.divider()

        # Voice Input
        audio_val = st.audio_input("🔴 Press to Speak / Reply")
        
        if audio_val:
            # Check if this audio is new (prevents duplication loop)
            # We use the size of the bytes as a simple signature check or just process it
            
            with st.spinner("Processing Voice..."):
                # 1. Transcribe (Returns Text Only)
                text = brain.transcribe_audio(audio_val.read())
                
                # DUPLICATION CHECK: Only append if it's not the exact same as the last user message
                # (Streamlit sometimes re-sends the same audio on refresh)
                should_process = True
                if st.session_state.ivr_history:
                    last_msg = st.session_state.ivr_history[-1]
                    # If the last message was the AI, we check the one before that (User)
                    if last_msg['role'] == "assistant" and len(st.session_state.ivr_history) >= 2:
                        last_user_msg = st.session_state.ivr_history[-2]['content']
                        if text == last_user_msg:
                            should_process = False
                
                if should_process and text.strip():
                    # 1. Add User Voice Text
                    st.session_state.ivr_history.append({"role": "user", "content": text})
                    
                    # 2. Get AI Response
                    context, sources = brain.get_rag_context(text)
                    response = brain.generate_response(text, context)
                    
                    # 3. Add AI Response
                    st.session_state.ivr_history.append({"role": "assistant", "content": response})
                    
                    # 4. Refresh to show chat
                    st.rerun()