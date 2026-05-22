#!/usr/bin/env python3
# coding=utf-8
import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError
import requests
import pyttsx3
import sys

# ======== 配置区 ========
DEEPSEEK_API_KEY = "YOUR_API_KEY"  # 填入你的密钥
TOPIC_NAME = "/usb_cam/image_raw"  # 确保这里是机器人实际的摄像头话题名！


# ========================

class RobotFruitTester:
    def __init__(self):
        rospy.init_node("robot_fruit_tester", anonymous=True)
        self.bridge = CvBridge()

        # 初始化语音
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
        except Exception as e:
            rospy.logerr(f"❌ 语音引擎初始化失败: {e}")
            sys.exit(1)

        # 订阅话题（只订阅一次，防卡死）
        self.sub = rospy.Subscriber(TOPIC_NAME, Image, self.image_callback, queue_size=1)
        rospy.loginfo(f"✅ 节点已启动，正在等待机器人话题 [{TOPIC_NAME}] 的画面...")

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
            rospy.logerr(f"❌ DeepSeek 接口请求失败: {e}")
            return "对不起，我的网络好像开小差了，无法分析水果新鲜度。"

    def image_callback(self, msg):
        # 拿到图就注销订阅，防止疯狂重复拍照分析
        self.sub.unregister()
        rospy.loginfo("📸 成功捕获机器人画面，正在处理...")

        try:
            # 1. 转为OpenCV格式并保存
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            img_filename = "robot_fruit.jpg"
            cv2.imwrite(img_filename, cv_image)
            rospy.loginfo("✅ 照片已保存")

            # 2. 调用API
            rospy.loginfo("🤖 正在呼叫 DeepSeek 分析水果...")
            prompt = "请判断图片中的水果是否新鲜，用简短中文回答，说明理由，适合机器人语音播报。"
            result_text = self.call_deepseek_api(img_filename, prompt)

            rospy.loginfo(f"🍉 最终结果: {result_text}")

            # 3. 语音播报
            self.engine.say(result_text)
            self.engine.runAndWait()

        except CvBridgeError as e:
            rospy.logerr(f"❌ 图像转换报错：{e}")
        except Exception as e:
            rospy.logerr(f"❌ 未知报错：{e}")
        finally:
            # 干完活自动退出节点
            rospy.loginfo("🏁 任务完成，节点退出。")
            rospy.signal_shutdown("Task Complete")
            sys.exit(0)


if __name__ == "__main__":
    try:
        node = RobotFruitTester()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
