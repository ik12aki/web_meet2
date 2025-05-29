# # 会議ルーム名入力
# room_name = st.text_input("会議ルーム名（英数字推奨）", value="my-room")

# # Google Meetの案内
# if st.button("🔗 Google Meetを開く"):
#     st.markdown(f"👉 [Google Meetを開く](https://meet.google.com/new)", unsafe_allow_html=True)
#     st.info("Google Meetの新規会議が開きます。ルーム名はメンバーで共有してください。")

# st.markdown("---")

import streamlit as st
import os
import json
import uuid
from datetime import datetime
from streamlit_drawable_canvas import st_canvas
import os

CHAT_DIR = "data/chats"
os.makedirs(CHAT_DIR, exist_ok=True)

def load_chat(room):
    path = os.path.join(CHAT_DIR, f"chat_{room}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    else:
        return []

def save_chat(room, chat_data):
    path = os.path.join(CHAT_DIR, f"chat_{room}.json")
    with open(path, "w") as f:
        json.dump(chat_data, f, indent=2)


def app():
   
    st.header("📡 Webミーティング")
    st.title("🎥 Webミーティング") #（Jitsi）

    room = st.text_input("会議ルーム名を入力:", "my-meeting-room")

    if room:
        iframe_height = 950
        st.components.v1.html(f"""
            <iframe src="https://meet.jit.si/{room}"
                    allow="camera; microphone; fullscreen; display-capture"
                    style="height: {iframe_height}px; width: 100%; border: 0px;"></iframe>
        """, height=iframe_height)


