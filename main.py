from flask import Flask, render_template, request, jsonify
import os
import tempfile
from text_to_video.api.generative_language_api import GenerativeLanguageAPI
from text_to_video.api.generative_image_from_text import DalleImageGenerator
from text_to_video.api.generative_text_from_audio_api import GenerativeTextFromAudioAPI

app = Flask(__name__)

# Folder for saving audio recordings
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# API instances for reuse
generative_text_api = GenerativeLanguageAPI()
image_generator = DalleImageGenerator()
audio_transcriber = GenerativeTextFromAudioAPI()


@app.route('/')
def index():
    return render_template('index.html')


def validate_prompt(data):
    prompt_text = data.get('prompt_text')
    if not prompt_text:
        return jsonify({'error': 'No text for the prompt'}), 400
    return prompt_text


@app.route('/upload', methods=['POST'])
def upload_audio():
    return jsonify({'message': 'File uploaded successfully'}), 200


@app.route('/generate_content_natural_language', methods=['POST'])
def generate_content_text():
    data = request.get_json()
    prompt_text = validate_prompt(data)
    if isinstance(prompt_text, tuple):
        return prompt_text  # Returns error if necessary

    prompt_text_detailed = f"Create a summary in English with a max of 40 characters of this message: '{prompt_text}'."
    
    try:
        response = generative_text_api.generate_content(prompt_text_detailed)
        text_response = response['candidates'][0]['content']['parts'][0]['text']
        return jsonify({'text_response': text_response, 'language': "English"})
    except KeyError:
        return jsonify({'error': 'Error processing the API response'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/generate_content_image', methods=['POST'])
def generate_content_image():
    data = request.get_json()
    prompt_text = validate_prompt(data)
    if isinstance(prompt_text, tuple):
        return prompt_text

    prompt_text_detailed = (
        f"Create an image of a teacher using American Sign Language (ASL) to convey the following message: '{prompt_text}'. "
        "The images should be arranged in a grid format, each illustrating a unique sign part of the ASL sequence. "
        "Translate '{prompt_text}' into English and display as a subtitle below the grid."
    )
    try:
        image_url = image_generator.generate_image(prompt_text_detailed)
        translation_prompt = f"Translate the following text into English: '{prompt_text}'."
        
        response = generative_text_api.generate_content(translation_prompt)
        text_response = response['candidates'][0]['content']['parts'][0]['text']
        
        return jsonify({'text_response': text_response, 'image_url': image_url or "The image can't be generated"})
    except KeyError:
        return jsonify({'error': 'Error processing the API response'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/generate_content_natural_language_with_audio', methods=['POST'])
def generate_content_text_with_audio():
    if 'audio' not in request.files or request.files['audio'].filename == '':
        return jsonify({'error': 'No valid audio file provided'}), 400

    audio_file = request.files['audio']
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
        audio_file.save(temp_audio_file.name)
        temp_audio_path = temp_audio_file.name 

    try:
        transcript_prompt = "Give me a transcript of this audio file."
        summary_prompt = "Give me a summary of this audio file. Include emotions and environmental sound descriptions."

        response_transcript = audio_transcriber.transcribe_audio(temp_audio_path, transcript_prompt)
        response_summary = audio_transcriber.transcribe_audio(temp_audio_path, summary_prompt)

        os.remove(temp_audio_path)  # Cleans up the temporary file

        return jsonify({
            'text_response_summary': response_summary or "The summary can't be generated from the audio",
            'text_response_transcript': response_transcript or "The transcript can't be generated from the audio"
        })
    except KeyError:
        return jsonify({'error': 'Error processing the API response'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
