import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# OpenAI API에 접근할 함수 (대화 기록을 포함해서 보냄)
def ask_chatgpt(messages):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
    )
    return response.choices[0].message.content

# 대화 기록을 유지하기 위해 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

# 사용자 입력 받기 및 엔터 키로 전송 설정
def send_message():
    user_message = st.session_state.user_input
    if user_message:
        st.session_state.messages.append({"role": "user", "content": user_message})
        with st.spinner("응답 중..."):
            ai_message = ask_chatgpt(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": ai_message})
    st.session_state.user_input = ""

# Streamlit 웹 페이지 구성
st.set_page_config(page_title="ChatGPT와 대화하기", layout="wide")
st.title("ChatGPT와 대화하기")
st.markdown("""
    이 웹페이지를 통해 GPT-4 모델과 대화할 수 있습니다. 아래에 질문을 입력하세요.
""")

# 대화 내용을 표시할 컨테이너 생성
chat_container = st.container()

# 입력 필드를 페이지 하단에 고정
st.markdown("<br>" * 5, unsafe_allow_html=True)  # 여백 추가
input_container = st.container()

# 대화 내용 표시
with chat_container:
    for message in st.session_state.messages:
        if message["role"] != "system":
            if message["role"] == "user":
                st.markdown(f"**Human**: {message['content']}")
            elif message["role"] == "assistant":
                st.markdown(f"**AI**: {message['content']}")

# 사용자 입력 받기 (엔터로 전송되도록 설정)
with input_container:
    st.text_input("질문을 입력하세요:", key="user_input", on_change=send_message)

# 자동 스크롤을 위한 빈 요소 추가
st.empty()

# 페이지가 로드될 때 스크롤을 맨 아래로 이동
st.markdown("""
    <script>
        var body = window.parent.document.querySelector(".main");
        body.scrollTop = body.scrollHeight;
    </script>
    """, unsafe_allow_html=True)