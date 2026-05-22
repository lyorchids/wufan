import cv2
import os
import requests
import base64

DEEPSEEK_API_KEY = "sk-xxxx"

def call_deepseek_api(img_path, prompt):
    try:
        # 1. 把图片转为 Base64 编码
        with open(img_path, "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode("utf-8")

        url = "ttps://dashscope.aliyuncs.com/compatible-mode/v1"
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }

        # 2. 按 DeepSeek 官方格式构造请求体
        data = {
            "model": "deepseek-vl",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                    ]
                }
            ]
        }

        res = requests.post(url, headers=headers, json=data)
        res_json = res.json()
        return res_json["choices"][0]["message"]["content"]

    except Exception as e:
        print("❌ API调用失败：", e)
        print("服务器返回内容：", res.text if 'res' in locals() else "无")
        return "分析失败，请检查API密钥或网络"