import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
        /* =========================================
           WHATSAPP INTERFACE STYLING
           ========================================= */
        
        /* 1. Main Phone Container */
        .whatsapp-wrapper {
            border: 1px solid #d1d7db;
            border-radius: 10px;
            overflow: hidden;
            max-width: 600px;
            margin: auto;
            font-family: Helvetica, Arial, sans-serif;
            background-color: #E5DDD5;
            display: flex;
            flex-direction: column;
            height: 550px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }

        /* 2. Header (Green Bar) */
        .whatsapp-header {
            background-color: #075E54;
            color: white;
            padding: 15px;
            display: flex;
            align-items: center;
        }
        
        .profile-pic {
            width: 40px;
            height: 40px;
            background-color: #ffffff;
            border-radius: 50%;
            margin-right: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }

        /* 3. Chat Area */
        .wa-chat-window {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            /* WhatsApp Background Pattern */
            background-image: url('https://user-images.githubusercontent.com/15075759/28719144-86dc0f70-73b1-11e7-911d-60d70fcded21.png');
            background-color: #E5DDD5; 
        }

        /* 4. Chat Bubbles */
        .wa-bubble-user {
            background-color: #dcf8c6;
            color: #303030;
            padding: 8px 12px;
            border-radius: 8px 0 8px 8px;
            margin: 5px 0 5px auto;
            max-width: 75%;
            box-shadow: 0 1px 1px rgba(0,0,0,0.1);
            width: fit-content;
            display: block;
        }
        
        .wa-bubble-bot {
            background-color: #ffffff;
            color: #303030;
            padding: 8px 12px;
            border-radius: 0 8px 8px 8px;
            margin: 5px auto 5px 0;
            max-width: 75%;
            box-shadow: 0 1px 1px rgba(0,0,0,0.1);
            width: fit-content;
            display: block;
        }

        /* =========================================
           FEATURE PHONE STYLING
           ========================================= */
        .phone-body {
            background-color: #222;
            border-radius: 30px;
            padding: 20px;
            border: 4px solid #444;
            color: #0f0;
            font-family: 'Courier New', monospace;
            text-align: center;
            box-shadow: 10px 10px 20px rgba(0,0,0,0.5);
        }
        .screen-text {
            font-size: 16px;
            margin-bottom: 20px;
            background-color: #333;
            padding: 15px;
            border-radius: 5px;
            border: 2px inset #555;
        }
        .keypad {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 8px;
            margin-top: 15px;
        }
        .key {
            background-color: #555;
            color: white;
            padding: 12px;
            border-radius: 5px;
            text-align: center;
            font-size: 14px;
        }
    </style>
    """, unsafe_allow_html=True)