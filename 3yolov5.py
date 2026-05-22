#!/usr/bin/env python3
# coding=utf-8
import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError
import requests
import pyttsx3
import sys

# ======== 閰嶇疆鍖?========
DEEPSEEK_API_KEY = "YOUR_API_KEY"  # 濉叆浣犵殑瀵嗛挜
TOPIC_NAME = "/usb_cam/image_raw"  # 纭繚杩欓噷鏄満鍣ㄤ汉瀹為檯鐨勬憚鍍忓ご璇濋鍚嶏紒


# ========================

class RobotFruitTester:
    def __init__(self):
        rospy.init_node("robot_fruit_tester", anonymous=True)
        self.bridge = CvBridge()

        # 鍒濆鍖栬闊?
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
        except Exception as e:
            rospy.logerr(f"鉂?璇煶寮曟搸鍒濆鍖栧け璐? {e}")
            sys.exit(1)

        # 璁㈤槄璇濋锛堝彧璁㈤槄涓€娆★紝闃插崱姝伙級
        self.sub = rospy.Subscriber(TOPIC_NAME, Image, self.image_callback, queue_size=1)
        rospy.loginfo(f"鉁?鑺傜偣宸插惎鍔紝姝ｅ湪绛夊緟鏈哄櫒浜鸿瘽棰?[{TOPIC_NAME}] 鐨勭敾闈?..")

    def call_deepseek_api(self, img_path, prompt):
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}"}
        try:
            files = {"file": open(img_path, "rb")}
            data = {
                "model": "deepseek-vl",
                "prompt": prompt
            }
            res = requests.post(url, headers=headers, files=files, data=data, timeout=30)
            res.raise_for_status()
            return res.json()["choices"][0]["message"]["content"]
        except Exception as e:
            rospy.logerr(f"鉂?DeepSeek 鎺ュ彛璇锋眰澶辫触: {e}")
            return "瀵逛笉璧凤紝鎴戠殑缃戠粶濂藉儚寮€灏忓樊浜嗭紝鏃犳硶鍒嗘瀽姘存灉鏂伴矞搴︺€?

    def image_callback(self, msg):
        # 鎷垮埌鍥惧氨娉ㄩ攢璁㈤槄锛岄槻姝㈢柉鐙傞噸澶嶆媿鐓у垎鏋?
        self.sub.unregister()
        rospy.loginfo("馃摳 鎴愬姛鎹曡幏鏈哄櫒浜虹敾闈紝姝ｅ湪澶勭悊...")

        try:
            # 1. 杞负OpenCV鏍煎紡骞朵繚瀛?
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            img_filename = "robot_fruit.jpg"
            cv2.imwrite(img_filename, cv_image)
            rospy.loginfo("鉁?鐓х墖宸蹭繚瀛?)

            # 2. 璋冪敤API
            rospy.loginfo("馃 姝ｅ湪鍛煎彨 DeepSeek 鍒嗘瀽姘存灉...")
            prompt = "璇峰垽鏂浘鐗囦腑鐨勬按鏋滄槸鍚︽柊椴滐紝鐢ㄧ畝鐭腑鏂囧洖绛旓紝璇存槑鐞嗙敱锛岄€傚悎鏈哄櫒浜鸿闊虫挱鎶ャ€?
            result_text = self.call_deepseek_api(img_filename, prompt)

            rospy.loginfo(f"馃崏 鏈€缁堢粨鏋? {result_text}")

            # 3. 璇煶鎾姤
            self.engine.say(result_text)
            self.engine.runAndWait()

        except CvBridgeError as e:
            rospy.logerr(f"鉂?鍥惧儚杞崲鎶ラ敊锛歿e}")
        except Exception as e:
            rospy.logerr(f"鉂?鏈煡鎶ラ敊锛歿e}")
        finally:
            # 骞插畬娲昏嚜鍔ㄩ€€鍑鸿妭鐐?
            rospy.loginfo("馃弫 浠诲姟瀹屾垚锛岃妭鐐归€€鍑恒€?)
            rospy.signal_shutdown("Task Complete")
            sys.exit(0)


if __name__ == "__main__":
    try:
        node = RobotFruitTester()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
