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
    st.title("🎥 Web会議（Jitsi）")

    room = st.text_input("会議ルーム名を入力:", "my-meeting-room")

    if room:
        st.components.v1.html(f"""
            <iframe src="https://meet.jit.si/{room}"
                    allow="camera; microphone; fullscreen; display-capture"
                    style="height: 600px; width: 100%; border: 0px;"></iframe>
        """, height=600)
        
    # --- お絵かきキャンバス ---
    st.subheader("🖌️ ホワイトボード（描画）")
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # オレンジ半透明
        stroke_width=3,
        stroke_color="#000000",
        background_color="#ffffff",
        height=300,
        width=800,
        drawing_mode="freedraw",
        key="canvas"
    )

    # 描画がある場合に表示
    if canvas_result.image_data is not None:
        st.image(canvas_result.image_data, caption="現在のホワイトボード", use_container_width=True)


    # 消去ボタン（再読み込みでキャンバスリセット）
    if st.button("🧹 ホワイトボードをクリア"):
        st.experimental_rerun()

    
    # # --- チャット機能 ---
    # st.subheader("💬 ルームチャット")

    # username = st.text_input("あなたの名前", value="guest")

    # chat_history = load_chat(room)
    
    # # 表示：過去のチャット
    # for msg in chat_history[-20:]:  # 直近20件
    #     st.markdown(f"**{msg['user']}** ({msg['time']}): {msg['message']}")
    
    # # 入力欄
    # new_msg = st.text_input("メッセージを入力", key="chat_input")
    
    # if st.button("送信"):
    #     if new_msg.strip():
    #         chat_history.append({
    #             "user": username,
    #             "message": new_msg.strip(),
    #             "time": datetime.now().strftime("%H:%M:%S")
    #         })
    #         save_chat(room, chat_history)
    #         st.rerun()

