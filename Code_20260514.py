#!/usr/bin/env python
#
# RobotForAll www.robotforall.net
# Authors: Jeffrey Tan <i@jeffreytan.org>
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError
import base64
from openai import OpenAI

photo_taken = False

class ImageRecognition:
    def __init__(self):
        # ========== 这里改成 DeepSeek ==========
        self.client = OpenAI(
            api_key = "YOUR_API_KEY",  # 你的DeepSeek密钥
            base_url = "https://api.deepseek.com",  # 官方地址
        )
        
        self.bridge = CvBridge()
        # 相机话题（你现在用笔记本就改成 /usb_cam/image_raw）
        self.sub = rospy.Subscriber("/camera/color/image_raw", Image, self.image_callback)

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
            global photo_taken
            if photo_taken == False:
                cv2.imwrite("photo.png", cv_image)
                photo_taken = True
                rospy.loginfo("The photo is taken.")
                self.get_response()
        except CvBridgeError as e:
            print(e)

    def get_response(self):
        prompt = "What is in this image?"
        with open("photo.png", "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
        
        # ========== 模型改成 deepseek-chat ==========
        completion = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                    ],
                }
            ],
        )
        rospy.loginfo(completion.choices[0].message.content)
        
        cv_photo = cv2.imread("photo.png")
        cv2.imshow('Photo', cv_photo)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    rospy.init_node('image_recognition', anonymous=True)  # 加anonymous防止重名
    ImageRecognition()
    rospy.spin()
