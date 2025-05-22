import streamlit as st
import gazo
import video
import webmeet

st.set_page_config(page_title="WebMeeting App", layout="wide")

# ユーザー認証設定
USER_CREDENTIALS = {
    "admin": "password123",
    "guest": "guestpass"
}

# ログイン処理
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔐 ログイン")
    username = st.text_input("ユーザー名")
    password = st.text_input("パスワード", type="password")
    if st.button("ログイン"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.success("ログイン成功")
            st.rerun()
        else:
            st.error("ユーザー名またはパスワードが違います")
else:
    st.sidebar.title("📂 メニュー")
    page = st.sidebar.radio("ページ選択", ("Webミーティング", "画像投稿", "動画投稿"))

    if page == "Webミーティング":
        webmeet.app()
    elif page == "画像投稿":
        gazo.app()
    elif page == "動画投稿":
        video.app()
