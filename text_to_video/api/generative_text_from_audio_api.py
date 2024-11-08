import google.generativeai as genai
from text_to_video.config.settings import settings

class GenerativeTextFromAudioAPI:
    def __init__(self):
        genai.configure(api_key=settings.API_KEY)
     
    def transcribe_audio(self, audio, prompt):
        # Define el modelo generativo de Google a utilizar
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        # Cargar el archivo de audio y especificar el tipo MIME
        audio_file = genai.upload_file(audio)

        # Enviar el prompt y el archivo de audio al modelo generativo
        response = model.generate_content([prompt, audio_file])

        # Imprimir y devolver el texto transcrito o el resumen
        print(response.text)
        return response.text
