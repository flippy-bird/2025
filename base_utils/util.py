import cv2
import subprocess
import re
import os
import base64

def video_preprocess(input_video_path):
    pass


#  base 64 编码格式
def encode_image(image_path):
    """
    将指定路径的图片进行编码
    参数:
        image_path (str): 图片文件的路径
    返回:
        str: 编码后的图片字符串
    """
    # 读取图片
    image = cv2.imread(image_path)
    # 调整图片大小
    image_resized = resize(image)
    # 将图片编码为JPEG格式
    _, encoded_image = cv2.imencode(".jpg", image_resized)
    # 将编码后的图片转换为Base64字符串
    return base64.b64encode(encoded_image).decode("utf-8")


def resize(image):
    """
    调整图片大小以适应指定的尺寸。
    参数:
        image (numpy.ndarray): 输入的图片，格式为numpy数组。
    返回:
        numpy.ndarray: 调整大小后的图片。
    """
    # 获取图片的原始高度和宽度
    height, width = image.shape[:2]
    # 根据图片的宽高比确定目标尺寸
    if height < width:
        target_height, target_width = 480, 640
    else:
        target_height, target_width = 640, 480
    # 如果图片尺寸已经小于或等于目标尺寸，则直接返回原图片
    if height <= target_height and width <= target_width:
        return image
    # 计算新的高度和宽度，保持图片的宽高比
    if height / target_height < width / target_width:
        new_width = target_width
        new_height = int(height * (new_width / width))
    else:
        new_height = target_height
        new_width = int(width * (new_height / height))
    # 调整图片大小
    return cv2.resize(image, (new_width, new_height))


def delete_all_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            continue  # 如果是文件夹，跳过

def get_iframe_indices(video_path):
    command = [
        'ffprobe', '-select_streams', 'v', '-show_frames',
        '-show_entries', 'frame=pkt_pts_time,pict_type',
        '-of', 'csv', video_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = result.stdout

    iframe_indices = []
    for line in output.split('\n'):
        if ',I' in line:
            match = re.search(r'frame,(\d*\.\d*),I', line)
            if match:
                time = float(match.group(1))
                iframe_indices.append(time)
    return iframe_indices


def extract_iframes(video_path, output_path):
    iframe_times = get_iframe_indices(video_path)
    cap = cv2.VideoCapture(video_path)

    if len(os.listdir(output_path)):
        delete_all_files_in_folder(output_path)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for i, time in enumerate(iframe_times):
        cap.set(cv2.CAP_PROP_POS_MSEC, time * 1000)  # 设置到指定时间位置
        ret, frame = cap.read()
        if ret:
            frame_filename = os.path.join(output_path, f'{i}.jpg')
            cv2.imwrite(frame_filename, frame)

    cap.release()


def get_frames(video_path, output_path):
    # 首选选取I帧作为参考
    if len(os.listdir(output_path)) > 0:
        delete_all_files_in_folder(output_path)
    extract_iframes(video_path, output_path)
    i_frames_num = len(os.listdir(output_path))
    # 如果I帧数量过少:
    if i_frames_num < 4:
        pass

    # 如果I帧数量过多：
    if i_frames_num > 15:
        pass


if __name__ == "__main__":
    # 示例使用
    video_path = r'../1_test_resources/1.mp4'
    output_path = '../output_frames'
    extract_iframes(video_path, output_path)
