import streamlit as st
import requests
import time

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent


def display_existing_messages():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def add_user_message_to_session(user_message):
    if user_message:
        st.session_state["messages"].append({"role": "user", "content": user_message})
        with st.chat_message("user"):
            st.markdown(user_message)


def assistant_response(query):
    url = "http://172.17.0.3:8100/chatbot/respond"

    # POST 요청에 포함될 데이터 (JSON 형식)
    data = {"query": query}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json().get("answer")
    else:
        return "오류가 발생했습니다. 다시 시도해주세요."


def main():
    st.title("인공지능 위로 챗봇 오복이")

    st.image(str(BASE_DIR.joinpath("assets", "charactor.png")), width=200)
    st.write("안녕하세요! 저는 인공지능 위로봇 '오복이'입니다.")
    st.write("우울한 마음을 위로해 드릴게요!")
    st.markdown("---")

    st.sidebar.title("Kakao Channel")
    st.sidebar.markdown("[카카오톡채널 - 위로봇 오복이](http://pf.kakao.com/_BNZRb)")

    st.sidebar.title("Donate")
    st.sidebar.write("<카카오뱅크> 3333095537425 오종민")
    st.sidebar.markdown("[Donate via KakaoPay](https://qr.kakaopay.com/FIgIytWbv)")

    st.sidebar.title("Contact")
    st.sidebar.write("alswhddh@naver.com")

    display_existing_messages()

    query = st.chat_input("궁금한 점이나 당신의 고민을 적어주세요.")
    if query:
        add_user_message_to_session(query)
        # Augment the query and generate assistant response
        with st.spinner("생각중..."):
            augmented_query = query
            response = assistant_response(augmented_query)
            time.sleep(3)
            st.session_state["messages"].append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)


if __name__ == "__main__":
    main()
