import pytest
from text_to_video.api.generative_language_api import GenerativeLanguageAPI

@pytest.fixture
def api():
    return GenerativeLanguageAPI()

def test_generate_content_success(mocker, api):
    # Configurar el mock para simular una respuesta exitosa de la API
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "content": "This is a generated response from the AI."
    }
    mocker.patch("requests.post", return_value=mock_response)

    # Llamar al método y verificar el resultado
    result = api.generate_content("Explain how AI works")
    assert result == {"content": "This is a generated response from the AI."}

def test_generate_content_api_error(mocker, api):
    # Configurar el mock para simular un error 500 de la API
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mocker.patch("requests.post", return_value=mock_response)

    # Verificar que se lance una excepción en caso de error de la API
    with pytest.raises(Exception) as exc_info:
        api.generate_content("Explain how AI works")
    
    assert "Error 500" in str(exc_info.value)
    assert "Internal Server Error" in str(exc_info.value)

def test_generate_content_authentication_error(mocker, api):
    # Configurar el mock para simular un error 403 (prohibido) de la API
    mock_response = mocker.Mock()
    mock_response.status_code = 403
    mock_response.text = "Forbidden: Invalid API Key"
    mocker.patch("requests.post", return_value=mock_response)

    # Verificar que se lance una excepción en caso de error de autenticación
    with pytest.raises(Exception) as exc_info:
        api.generate_content("Explain how AI works")
    
    assert "Error 403" in str(exc_info.value)
    assert "Forbidden: Invalid API Key" in str(exc_info.value)
