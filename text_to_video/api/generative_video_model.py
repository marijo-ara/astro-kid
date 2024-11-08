import json
import requests
from text_to_video.config.settings import settings

class GoogleImagenVideo:
    def __init__(self):
        """Initialize the class with the API key."""
        self.api_key = settings.API_KEY
        self.base_url = "https://api.google.com/imagen_video"  # Hypothetical endpoint

    def generate_video(self, input_text: str) -> str:
        """Generate a video from the input text."""
        url = f"{self.base_url}/generate_video?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "input_text": input_text
        }

        # Make the POST request to generate the video
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            # Assuming the response contains a URL to the generated video
            video_url = response.json().get("video_url")
            return video_url
        else:
            raise Exception(f"Error generating video: {response.status_code} - {response.text}")

    def download_video(self, video_url: str, output_file: str) -> None:
        """Download the generated video to a local file."""
        response = requests.get(video_url, stream=True)

        if response.status_code == 200:
            with open(output_file, "wb") as out_file:
                for chunk in response.iter_content(chunk_size=8192):
                    out_file.write(chunk)
            print(f"Video downloaded successfully: {output_file}")
        else:
            raise Exception(f"Error downloading video: {response.status_code} - {response.text}")
