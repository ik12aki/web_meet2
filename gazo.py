import streamlit as st
import os
import json
import uuid
import datetime
from collections import defaultdict

def app():
    st.title("🖼️ 画像投稿")

    UPLOAD_DIR = "uploads/images"
    POSTS_FILE = "data/posts.json"

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, "w") as f:
            json.dump({"posts": []}, f)

    def load_posts():
        with open(POSTS_FILE, "r") as f:
            return json.load(f)["posts"]

    def save_all_posts(posts):
        with open(POSTS_FILE, "w") as f:
            json.dump({"posts": posts}, f, indent=2)

    def save_post(user, filenames, comment, public, media_type):
        posts = load_posts()
        posts.append({
            "id": str(uuid.uuid4()),
            "user": user,
            "filenames": filenames,
            "comment": comment,
            "public": public,
            "type": media_type,
            "date": datetime.date.today().isoformat(),
            "comments_on_post": []
        })
        save_all_posts(posts)

    uploaded_files = st.file_uploader("画像を選択（複数可）", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    if uploaded_files:
        comment = st.text_area("この投稿へのコメント")
        public = st.checkbox("公開する", value=True)
        if st.button("投稿する"):
            saved_files = []
            for file in uploaded_files:
                filepath = os.path.join(UPLOAD_DIR, file.name)
                with open(filepath, "wb") as f:
                    f.write(file.read())
                saved_files.append(file.name)
            save_post(st.session_state["username"], saved_files, comment, public, "image")
            st.success("投稿を保存しました")
            st.rerun()

    # 投稿一覧表示
    st.header("📅 投稿一覧")
    posts = load_posts()
    posts_by_date = defaultdict(list)
    for post in posts:
        if post["type"] != "image":
            continue
        if not post.get("public", True) and post["user"] != st.session_state["username"]:
            continue
        posts_by_date[post.get("date", "不明な日付")].append(post)

    for date, posts_on_date in sorted(posts_by_date.items(), reverse=True):
        st.subheader(f"📆 {date}")
        for post in posts_on_date:
            st.write(f"👤 投稿者: {post['user']}")
            for fname in post["filenames"]:
                path = os.path.join(UPLOAD_DIR, fname)
                if os.path.exists(path):
                    st.image(path, width=300)
            st.markdown(f"💬 投稿コメント: {post['comment']}")
            for c in post["comments_on_post"]:
                st.write(f"- {c}")
            new_comment = st.text_input("コメントを書く", key=f"cmt_{post['id']}")
            if st.button("コメント投稿", key=f"btn_{post['id']}"):
                if new_comment.strip():
                    post["comments_on_post"].append(new_comment.strip())
                    save_all_posts(posts)
                    st.rerun()
            if post["user"] == st.session_state["username"]:
                if st.button("🗑️ 削除", key=f"del_{post['id']}"):
                    for fname in post["filenames"]:
                        try:
                            os.remove(os.path.join(UPLOAD_DIR, fname))
                        except:
                            pass
                    posts = [p for p in posts if p["id"] != post["id"]]
                    save_all_posts(posts)
                    st.rerun()
