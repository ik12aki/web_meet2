# import streamlit as st

# def app():
#     st.header("📡 Webミーティング")
#     st.title("🎥 Web会議（Jitsi）")

#     room = st.text_input("会議ルーム名を入力:", "my-meeting-room")

#     if room:
#         st.components.v1.html(f"""
#             <iframe src="https://meet.jit.si/{room}"
#                     allow="camera; microphone; fullscreen; display-capture"
#                     style="height: 600px; width: 100%; border: 0px;"></iframe>
#         """, height=600)

import streamlit as st
import os
import json
import uuid
from datetime import datetime

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
    st.set_page_config(page_title="Webミーティング", layout="wide")
    st.header("📡 Webミーティング")
    st.title("🎥 Google Meet + チャット")

    # 会議ルーム名入力
    room_name = st.text_input("会議ルーム名（英数字推奨）", value="my-room")

    # Google Meetの案内
    if st.button("🔗 Google Meetを開く"):
        st.markdown(f"👉 [Google Meetを開く](https://meet.google.com/new)", unsafe_allow_html=True)
        st.info("Google Meetの新規会議が開きます。ルーム名はメンバーで共有してください。")

    st.markdown("---")

    # --- チャット機能 ---
    st.subheader("💬 ルームチャット")

    username = st.text_input("あなたの名前", value="guest")

    chat_history = load_chat(room_name)

    # 表示：過去のチャット
    for msg in chat_history[-20:]:  # 直近20件
        st.markdown(f"**{msg['user']}** ({msg['time']}): {msg['message']}")

    # 入力欄
    new_msg = st.text_input("メッセージを入力", key="chat_input")

    if st.button("送信"):
        if new_msg.strip():
            chat_history.append({
                "user": username,
                "message": new_msg.strip(),
                "time": datetime.now().strftime("%H:%M:%S")
            })
            save_chat(room_name, chat_history)
            st.rerun()
