import cv2
import base64
import requests
import pyttsx3
import os
import time

# ===================== 配置区（必须填）=====================
QWEN_API_KEY = "sk-435bb67e9a1f45038c8391a4f2ce16b6"  # 去阿里云百炼获取
# ==========================================================
engine = pyttsx3.init()
def take_photo():
    """笔记本摄像头拍照"""
    print("📸 打开摄像头，按 S 拍照，按 Q 退出")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ 打不开摄像头")
        return None

    img_path = "fresh.jpg"
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Camera - S拍照 Q退出", frame)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('s'):
            cv2.imwrite(img_path, frame)
            print("✅ 拍照完成")
            break
        if k == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return None

    cap.release()
    cv2.destroyAllWindows()
    return img_path

def qwen_fresh_analyze(img_path):
    """通义千问视觉模型分析果蔬新鲜度"""
    try:
        with open(img_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()

        url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {QWEN_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "qwen-vl-plus",
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "text", "text": "请分析果蔬新鲜度，给出：1.新鲜等级 2.外观状态 3.是否可食用 4.建议。口语化"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                ]
            }]
        }

        resp = requests.post(url, headers=headers, json=data)
        j = resp.json()
        if "choices" in j:
            return j["choices"][0]["message"]["content"]
        else:
            return "分析失败：" + str(j)
    except Exception as e:
        return "错误：" + str(e)



def main():
    print("🍎 通义千问果蔬新鲜度识别")
    print("="*40)
    
    path = take_photo()
    if not path:
        return

    print("🔍 正在分析...")
    res = qwen_fresh_analyze(path)
    print("\n📊 分析结果：")
    print(res)
    if res:
        text = res
        engine.say(text)
    
    if os.path.exists(path):
        os.remove(path)

if __name__ == "__main__":
    main()