import cv2
import base64
import requests
import pyttsx3
import os
import time

# ===================== 閰嶇疆鍖猴紙蹇呴』濉級=====================
QWEN_API_KEY = "YOUR_API_KEY"  # 鍘婚樋閲屼簯鐧剧偧鑾峰彇
# ==========================================================
engine = pyttsx3.init()
def take_photo():
    """绗旇鏈憚鍍忓ご鎷嶇収"""
    print("馃摳 鎵撳紑鎽勫儚澶达紝鎸?S 鎷嶇収锛屾寜 Q 閫€鍑?)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("鉂?鎵撲笉寮€鎽勫儚澶?)
        return None

    img_path = "fresh.jpg"
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Camera - S鎷嶇収 Q閫€鍑?, frame)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('s'):
            cv2.imwrite(img_path, frame)
            print("鉁?鎷嶇収瀹屾垚")
            break
        if k == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return None

    cap.release()
    cv2.destroyAllWindows()
    return img_path

def qwen_fresh_analyze(img_path):
    """閫氫箟鍗冮棶瑙嗚妯″瀷鍒嗘瀽鏋滆敩鏂伴矞搴?""
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
                    {"type": "text", "text": "璇峰垎鏋愭灉钄柊椴滃害锛岀粰鍑猴細1.鏂伴矞绛夌骇 2.澶栬鐘舵€?3.鏄惁鍙鐢?4.寤鸿銆傚彛璇寲"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                ]
            }]
        }

        resp = requests.post(url, headers=headers, json=data)
        j = resp.json()
        if "choices" in j:
            return j["choices"][0]["message"]["content"]
        else:
            return "鍒嗘瀽澶辫触锛? + str(j)
    except Exception as e:
        return "閿欒锛? + str(e)



def main():
    print("馃崕 閫氫箟鍗冮棶鏋滆敩鏂伴矞搴﹁瘑鍒?)
    print("="*40)
    
    path = take_photo()
    if not path:
        return

    print("馃攳 姝ｅ湪鍒嗘瀽...")
    res = qwen_fresh_analyze(path)
    print("\n馃搳 鍒嗘瀽缁撴灉锛?)
    print(res)
    if res:
        text = res
        engine.say(text)
    
    if os.path.exists(path):
        os.remove(path)

if __name__ == "__main__":
    main()
