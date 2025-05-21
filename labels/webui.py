import gradio as gr
from qwen_vl import VideoAnalysis

video_rec = VideoAnalysis()

with gr.Blocks() as demo:
    gr.Markdown("素材识别工具")

    with gr.Tabs():
        with gr.Tab("🔍 文字素材打标"):
            gr.Markdown("### 请上传文字素材文件")
            file_input = gr.File(label="上传文字素材文件")
            check_button = gr.Button("开始分析")
            image_display = gr.Image(label="预览图片", type="filepath")  # 添加图片显示组件
            check_output = gr.Textbox(label="打标结果")
            # 更新图片显示和打标结果的回调逻辑
            check_button.click(lambda file: (file, video_rec.rec_all_in_one(file, 1)), inputs=file_input, outputs=[image_display, check_output])

        with gr.Tab("🎨 非文字类素材风格打标"):
            gr.Markdown("### 请上传素材文件")
            file_input2 = gr.File(label="上传素材文件")
            check_button2 = gr.Button("开始分析")
            image_display2 = gr.Image(label="预览图片", type="filepath")  # 添加图片显示组件
            check_output2 = gr.Textbox(label="打标结果")
            # 更新图片显示和打标结果的回调逻辑
            check_button2.click(lambda file: (file, video_rec.rec_all_in_one(file, 2)), inputs=file_input2, outputs=[image_display2, check_output2])

        # with gr.Tab("🎅 非文字类素材节日打标"):
        #     gr.Markdown("### 请上传素材文件")
        #     file_input2 = gr.File(label="上传素材文件")
        #     check_button2 = gr.Button("开始分析")
        #     image_display2 = gr.Image(label="预览图片", type="filepath")  # 添加图片显示组件
        #     check_output2 = gr.Textbox(label="打标结果")
        #     # 更新图片显示和打标结果的回调逻辑
        #     check_button2.click(lambda file: (file, video_rec.rec(file, 3)), inputs=file_input2, outputs=[image_display2, check_output2])

        # with gr.Tab("🎯 非文字类素材元素打标"):
        #     gr.Markdown("### 请上传素材文件")
        #     file_input2 = gr.File(label="上传素材文件")
        #     check_button2 = gr.Button("开始分析")
        #     image_display2 = gr.Image(label="预览图片", type="filepath")  # 添加图片显示组件
        #     check_output2 = gr.Textbox(label="打标结果")
        #     # 更新图片显示和打标结果的回调逻辑
        #     check_button2.click(lambda file: (file, video_rec.rec(file, 4)), inputs=file_input2, outputs=[image_display2, check_output2])

demo.launch(server_name="0.0.0.0", server_port=7860)