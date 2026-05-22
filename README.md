# 机器人视觉识别 —— 果蔬新鲜度检测系统

> 机器人课程（RobotForAll）课程作业

## 项目简介

本项目是机器人课程的课程作业，实现基于 **ROS（Robot Operating System）** 的机器人视觉识别功能，结合大语言模型（LLM）的视觉理解能力，对摄像头采集的果蔬图像进行**新鲜度分析**，并通过语音合成（TTS）播报分析结果。

项目探索了两种主流视觉语言模型：

| 模型 | 服务商 | API 模式 |
|------|--------|----------|
| **DeepSeek VL** | DeepSeek 官方 | OpenAI 兼容接口 |
| **通义千问 Qwen VL** | 阿里云百炼 | OpenAI 兼容接口 |

## 文件说明

| 文件 | 说明 |
|------|------|
| `3yolov5.py` | **ROS 节点**，订阅机器人摄像头话题 → DeepSeek VL 分析果蔬新鲜度 → TTS 语音播报。获取一张图片后自动取消订阅并退出 |
| `Code_20260514.py` | **ROS 节点**（基于 RobotForAll 模板改造），使用 DeepSeek（OpenAI SDK）进行图像识别，并 OpenCV 显示结果 |
| `image_recognition_qwen.py` | **ROS 节点**（基于 RobotForAll 模板改造），使用 Qwen VL（阿里云百炼）进行图像识别 |
| `Qwenf.py` | **本机摄像头版**，调用电脑摄像头拍照 → Qwen VL 分析果蔬新鲜度 → TTS 语音播报 |
| `Code_20260522.py` | **工具函数**，封装 DeepSeek VL API 调用（Base64 传图），通用模块 |
| `deepseek_ff.py` | **工具函数**，封装通义千问 VL API 调用（Base64 传图），通用模块 |

## 依赖

- Python 3
- ROS（运行 ROS 节点时需要）
- `rospy`、`cv_bridge`（ROS 节点必需）
- `opencv-python`
- `requests`
- `pyttsx3`（文本转语音）
- `openai`（OpenAI SDK 方式时使用）

## 快速开始

### 1. 配置 API 密钥

在对应脚本的配置区填入你的 API Key：

- **DeepSeek**：https://platform.deepseek.com/
- **阿里云百炼（Qwen）**：https://bailian.console.aliyun.com/

### 2. 运行 ROS 节点（机器人类）

```bash
# 确保 ROS Master 已启动
rosrun your_package 3yolov5.py
# 或
rosrun your_package Code_20260514.py
```

脚本会自动订阅摄像头话题（默认 `/usb_cam/image_raw` 或 `/camera/color/image_raw`），捕获画面后调用视觉模型分析并语音播报结果。

### 3. 运行本机摄像头版

```bash
python Qwenf.py
```

按 `S` 拍照，按 `Q` 退出，程序会自动分析并语音播报。

## 课程信息

- **平台**：RobotForAll（www.robotforall.net）
- **作者**：Jeffrey Tan <i@jeffreytan.org>（模板作者）
