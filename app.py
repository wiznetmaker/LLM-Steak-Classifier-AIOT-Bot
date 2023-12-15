from openai import OpenAI
import dotenv
import os
import base64
import requests
import socket
import streamlit as st
from function import *

HOST = "192.168.11.146"  # Standard loopback interface address (localhost)
PORT = 50007  # Port to listen on (non-privileged ports are > 1023)

api_key = "Your API Key"

client = OpenAI(api_key=api_key)
st.set_page_config(layout="wide")
col1, col2, col3 = st.columns([1, 6, 1])


with col2:
    # 레이아웃 및 스타일링 설정
    st.title("LLM Steak Classifier AIOT Bot - 🥩 WIZnet Steak House 🥩")  # 이모티콘 추가
    # 설명 텍스트 스타일링
    st.markdown(
        """
        <div style= padding: 10px; border-radius: 5px;">
            <span style="color: red; font-size: 16px;">
                🤖 이 봇은 GPT-Vision LLM 기반의 추론을 통해 고기의 익음 정도를 판별해 드립니다.
            </span>
        </div>
    """,
        unsafe_allow_html=True,
    )
    st.image(
        "Capture Image Path",
        width=1500,
    )

    # 이미지 업로드
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("📸 사진을 업로드 하세요", type=["jpg", "png"])
    with col2:
        if uploaded_file:
            st.image(uploaded_file, caption="업로드된 이미지")

    if uploaded_file is not None:
        # 업로드된 이미지를 base64 인코딩
        user_base64_image = upload_encode_image(uploaded_file)

    if uploaded_file is not None:
        image_path = "image/img.png"

        base64_image = encode_image(image_path)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        system_message = read_prompt("prompts/system_prompt.txt")
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": system_message + "What’s in this image?",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            "max_tokens": 300,
            "temperature": 0.1,
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
        )

        print(response.json())
        # 고기를 참고할 수 있는 정보의 컨텍스트를 만들어준다.
        context = response.json()["choices"][0]["message"]["content"]

        main_prompt = read_prompt("prompts/main_prompt.txt")

        st.write(f"고기의 온도를 측정하기 위해 대기중입니다... 온도계 연결해주세요 🥩")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
            server_socket.listen()
            print(f"서버 {HOST}:{PORT} 대기 중입니다.")

            while True:
                conn, addr = server_socket.accept()

                with conn:
                    print(f"{addr}에서 연결됨.")
                    data = conn.recv(1024)  # 클라이언트로부터 데이터 수신
                    temp = float(data.decode())
                    break

        temp = data
        if temp < 52:
            grade = "Undercooked"
        elif temp < 57:
            grade = "Rare"
        elif temp < 63:
            grade = "Medium Rare"
        elif temp < 74:
            grade = "Medium"
        else:
            grade = "Well Done"

        st.write(f"Real Steak template: {temp}도, {grade} 🥩")
        user_question = st.text_input("🤔 고기의 익음 정도를 알고 싶은 질문을 입력하세요.")
        if st.button("🚀 전송"):
            sys_prompt = context + "\n\n" + main_prompt + "\n\n" + user_question

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            }

            payload = {
                "model": "gpt-4-vision-preview",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": sys_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{user_base64_image}"
                                },
                            },
                        ],
                    }
                ],
                "max_tokens": 300,
                "temperature": 0,
            }

            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
            )

            if response.ok:
                result_content = response.json()["choices"][0]["message"]["content"]
                st.markdown(
                    f"<div style='background-color: black; color: white; padding: 10px; border-radius: 5px;'>{result_content}</div>",
                    unsafe_allow_html=True,
                )
            else:
                # 오류 발생 시 메시지 출력
                st.error("오류가 발생했습니다: " + response.text)
