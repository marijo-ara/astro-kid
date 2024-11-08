from openai import OpenAI
from text_to_video.config.settings import settings

class DalleImageGenerator:
    def __init__(self):
         self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_image(self, prompt, model="dall-e-3", size="1024x1024", quality="standard", n=1):
        try:
            response = self.client.images.generate(
                model=model,
                prompt=prompt,
                size=size,
                quality=quality,
                n=n,
            )
            # Assuming only one image is generated, get the URL of the first one
            image_url = response.data[0].url
            return image_url
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
