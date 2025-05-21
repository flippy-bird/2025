from google.cloud import storage
import os
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
from pathlib import Path
from prompt import PROMPT_HUB
from openai import OpenAI
from config import *

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/pan/Documents/2025/github/video-understanding/resources/ai-2c-gemini.json"


def upload_to_gcs(source_file_name, destination_blob_name, bucket_name="ai-2c-video"):
    """Uploads a file to the bucket."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Upload the file
    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")
    return {
        "name": blob.name,
        "size": blob.size,
        "content_type": blob.content_type,
        "public_url": blob.public_url
    }

# source_file_name = "/home/pan/Documents/2025/github/video-understanding/test_resources/audios/1.m4a"
# destination_blob_name = "audios/1.m4a"



class AudioDectector:
    def __init__(self):
        ## qwen omni的设置
        self.qwen_omni_client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )


        ## gemini的设置
        vertexai.init(project="ai-2c-gemini", location="us-central1")
        self.model = GenerativeModel(
            "gemini-2.0-flash",
        )

        self.generation_config = {
            "max_output_tokens": 8192,
            "temperature": 1,
            "top_p": 0.95,
        }

        self.bucket_name = "ai-2c-video"

    def detect(self, audio_path):
        file_name = Path(audio_path).name
        destination_blob_name = f"audios/{file_name}"
        upload_to_gcs(audio_path, destination_blob_name, self.bucket_name)

        audio_url = f"gs://{self.bucket_name}/{destination_blob_name}"

        audio_file = Part.from_uri(audio_url, mime_type="audio/mp3")

        prompt_genre = PROMPT_HUB["music_genre"]
        prompt_music_instruments = PROMPT_HUB["music_instruments"]
        prompt_music_emotion = PROMPT_HUB["music_emotion"]
        prompt_gender = PROMPT_HUB["rec_music_gender"]

        res_genre = self.model.generate_content([audio_file, prompt_genre])
        res_emotion = self.model.generate_content([audio_file, prompt_music_emotion])
        res_instruments = self.model.generate_content([audio_file, prompt_music_instruments])
        res_gender = self.model.generate_content([audio_file, prompt_gender])

        print(res_genre.text)
        print(res_emotion.text)

        return {
            "genre": [res_genre.text.replace("```json", "").replace("```", "")],
            "emotion": res_emotion.text.replace("```json", "").replace("```", ""),
            "instruments": res_instruments.text.replace("```json", "").replace("```", ""),
            "gender": res_gender.text
        }
    
    def detect_by_QwenOmni(self, audio_path):
        pass
    
# audio_dector = AudioDectector()
# res = audio_dector.detect("/home/pan/Documents/2025/github/video-understanding/test_resources/audios/1.m4a")
# print(res["instruments"])
