import os
from openai import OpenAI
from PIL import Image
import base64
from io import BytesIO
import sys

print(os.getcwd())
sys.path.append(".")
sys.path.append("..")
from base_utils.util import *
from prompt_hub import get_text_prompt,get_style_prompt,get_festvial_prompt, get_element_prompt
from config import API_KEY, MODEL


def save_base64_to_image(base64_string, output_path):
    try:
        # 解码 Base64
        image_data = base64.b64decode(base64_string)

        # 将解码后的数据写入文件
        with open(output_path, 'wb') as f:
            f.write(image_data)
        print(f"图片已保存至: {output_path}")
    except Exception as e:
        print(f"转换失败: {e}")

num_global = 0

class VideoAnalysis:
    def __init__(self):
        self.__client = OpenAI(
            api_key=API_KEY,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

        # self.reference_message = self.rec_with_reference()

    def rec(self, input_path, mode):
        file_name = os.path.basename(input_path)
        # 区分视频还是图片
        ext = file_name.split(".")[1]
        prompt = ""
        frames = None

        image_prompt = ""
        video_prompt = ""
        if mode == 1:
            image_prompt = get_text_prompt("图片")
            video_prompt = get_text_prompt("视频")
        if mode == 2:
            image_prompt = get_style_prompt("图片")
            video_prompt = get_style_prompt("视频")
        if mode == 3:
            image_prompt = get_festvial_prompt("图片")
            video_prompt = get_festvial_prompt("视频")
        if mode == 4:
            image_prompt = get_element_prompt("图片")
            video_prompt = get_element_prompt("视频")

        image_ext = "jpeg"
        if ext in ["jpg", "jpeg", "png"]:
            frames = self._deal_image(input_path)
            prompt = image_prompt
            if ext == "png":
                image_ext = ext
        elif ext in ["mp4", "mov", "MP4", "avi", "MOV"]:
            frames = self._deal_video(input_path)
            prompt = video_prompt
        elif ext in ["webp", "WEBP"]:
            frames = self._deal_webp(input_path)
            # webp使用 中间一帧好了
            # count = len(frames)
            # frames = [frames[count // 2]]
            # global  num_global
            # save_base64_to_image(frames[0], f"./{num_global}.jpg")
            # num_global += 1
            prompt = video_prompt
        if len(frames) == 1:
            prompt = image_prompt
        res = self._scene_rec(prompt, frames, image_ext)
        return res

    def _scene_rec(self, prompt, base64_images, image_ext, need_reference=False):
        video_url = []
        messages = []
        for base64_image in base64_images:
            video_url.append(f"data:image/{image_ext};base64,{base64_image}")

        # prompt = "示例中的第四张图片是什么风格？注意我问的是之前示例中的图片"

        if len(video_url) > 1:
            content = [
                    {"type": "video", "video": video_url},
                    {"type": "text", "text": prompt}]
        else:
            content = [
                    {"type": "image_url", "image_url": {"url": video_url[0]}},
                    {"type": "text", "text": prompt},
                ]

        # content = [
        #     {"type": "text", "text": prompt},
        # ]

        # 这里启动了实例参考功能
        if need_reference:
            ref_messages = self.reference_message
            # messages.append(ref_messages[0])
            ref_messages.append({"role": "user", "content": content})
            messages = ref_messages
        else:
            messages.append({"role": "user", "content": content})

        completion = self.__client.chat.completions.create(
            model="qwen-vl-max-latest",
            messages=messages
        )

        res = completion.choices[0].message.content
        print(completion.usage.total_tokens)

        return res

    def _deal_webp(self, image_path):
        image = Image.open(image_path)

        # 遍历并保存所有帧
        frames = []
        frame_number = 0
        while True:
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            image_bytes = buffer.getvalue()
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
            frames.append(image_base64)  # 可改为 "WEBP" 或 "JPEG"
            frame_number += 1
            try:
                image.seek(frame_number)  # 移动到下一帧
            except EOFError:
                break  # 结束
        return frames

    def _deal_video(self, input_path):
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            print("无法打开视频文件")
            exit()

        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_resized = resize(frame)
            _, encoded_image = cv2.imencode(".jpg", frame_resized)
            frames.append(base64.b64encode(encoded_image).decode("utf-8"))
        # 因为千问大模型最多支持80张图片，所以这里需要操作
        num = len(frames)
        divide = 1
        if num > 80:
            divide = int(num / 80) + 1
        frames = frames[::divide]

        return frames

    def _deal_image(self, image_path):
        frames = []
        with open(image_path, "rb") as file:
            base64_image = base64.b64encode(file.read()).decode("utf-8")
        frames.append(base64_image)
        return frames
    
    def rec_with_reference(self):
        reference_images_path = "/media/pan/新加卷/模型训练数据/标签分类/风格/example_label_image/"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
        
        def list_sorted_files(directory):
            # 获取所有文件名，并过滤掉非文件项
            files = [f for f in os.listdir(directory) if f.endswith(".png")]
            # 使用数字排序
            sorted_files = sorted(files, key=lambda x: int(os.path.splitext(x)[0]))
            return sorted_files

        content = []
        files = list_sorted_files(reference_images_path)
        text = ""
        # for file in files:
        for i in range(len(files)):
            file = files[i]
            reference_image_path = os.path.join(reference_images_path, file)
            base64_image = encode_image(reference_image_path)
            content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}})
            file_name = os.path.splitext(file)[0]
            label_file_path = os.path.join(reference_images_path, f"{file_name}.txt")
            with open(label_file_path, "r") as f:
                label = f.read()
            text += f"第{i+1}张图片的风格标签是：{label}\n"

        text += "上面给了你一些参考图片以及对应的风格标签，后面我会给你一个图片或者视频，请参考上面的示例进行打标。请回答是或者否表示理解了我的需求。"
        content.append({"type": "text", "text": text})
        print(text)

        messages = [{"role":"system","content":[{"type": "text", "text": "你是一个打标员，能够结合示例的打标情况，给新输入的视频或者图片打标"}]},
                {"role": "user", "content": content}]
        completion = self.__client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        print(f"第一轮输出:{completion.choices[0].message.content}")
        assistant_message = completion.choices[0].message
        print(f"参考使用token: {completion.usage.total_tokens}")
        messages.append(assistant_message.model_dump())
        return messages
    

if __name__ == "__main__":
    video = VideoAnalysis()
    # test_dir = "/home/pan/Downloads/文字/"
    # log_file = open("./log_0327.txt", "w")
    # files = os.listdir(test_dir)
    # for file in files:
    #     file_path = os.path.join(test_dir, file)
    #     res = video.rec(file_path, 1)
    #     log_file.write(f"{file}: {res}")
    #     log_file.write("\n")

    # log_file.close()

    test_path = "/home/pan/Downloads/文字/10.webp"
    res = video.rec(test_path, 3)
    print(res)
