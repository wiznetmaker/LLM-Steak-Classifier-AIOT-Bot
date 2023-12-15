from openai import OpenAI
import dotenv
import os
import base64
import requests


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
  
def upload_encode_image(uploaded_file):
    # 업로드된 파일의 바이트 데이터를 base64 인코딩으로 변환
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
  
def read_prompt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        prompt = file.read()
    return prompt

def user_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
  
  