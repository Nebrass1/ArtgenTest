# Fichier: generator/tests/test_generator_api.py (Code Complet et Corrigé)

import pytest
from unittest.mock import patch, Mock
from django.urls import reverse
from django.test import Client
from requests.exceptions import Timeout
import base64


@pytest.fixture
def client():
    return Client()


# Créer une image PNG BEAUCOUP plus grande
def create_large_test_image():
    """Crée une image PNG de test très grande"""
    from PIL import Image
    import io
    import random
    
    # Créer une image 500x500 pixels avec du bruit aléatoire
    img = Image.new('RGB', (500, 500))
    pixels = img.load()
    
    # Remplir avec des pixels aléatoires pour maximiser la taille
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixels[i, j] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    img_io = io.BytesIO()
    img.save(img_io, 'PNG', optimize=False)  # Désactiver l'optimisation
    img_io.seek(0)
    content = img_io.getvalue()
    print(f"Created test image size: {len(content)} bytes")
    return content

LARGE_PNG_CONTENT = create_large_test_image()


# Simuler une réponse d'API réussie (pour HuggingFace)
def mock_successful_response(*args, **kwargs):
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.content = LARGE_PNG_CONTENT
    return mock_resp


@patch('generator.views.requests.post', side_effect=mock_successful_response)
def test_generation_success(mock_post, client):
    """TC-GEN-01: Test de generation reussie avec l'API principale (HuggingFace)"""
    
    prompt_data = {
        'prompt': 'A mystical cybernetic cat in a rainy city',
        'style': 'Cyberpunk'
    }
    
    response = client.post(reverse('generate_image'), data=prompt_data)
    
    assert mock_post.called
    assert response.status_code == 200
    assert 'image_data' in response.context
    assert len(response.context['image_data']) > 100


# Simuler l'échec de l'API (e.g., erreur 500 ou Timeout)
def mock_failed_response(*args, **kwargs):
    mock_resp = Mock()
    mock_resp.status_code = 500
    return mock_resp


@patch('generator.views.requests.post', side_effect=mock_failed_response)
def test_generation_api_failure_500(mock_post, client):
    """TC-GEN-02a: L'API principale retourne 500, verification de la gestion de l'erreur."""
    
    prompt_data = {
        'prompt': 'A non-existent prompt',
        'style': 'Error Style'
    }
    
    response = client.post(reverse('generate_image'), data=prompt_data)
    
    assert response.status_code == 200
    assert 'error' in response.context


@patch('generator.views.requests.post', side_effect=Timeout)
def test_generation_api_timeout(mock_post, client):
    """TC-GEN-02b: L'API principale fait un timeout, verification de la gestion de l'erreur."""
    
    prompt_data = {
        'prompt': 'A prompt for timeout',
        'style': 'Timeout Style'
    }
    
    response = client.post(reverse('generate_image'), data=prompt_data)
    
    assert response.status_code == 200
    assert 'error' in response.context


# Simuler la réponse de succès pour Pollinations (GET)
def mock_successful_pollinations_response(*args, **kwargs):
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.content = LARGE_PNG_CONTENT
    return mock_resp


@patch('generator.views.requests.get', side_effect=mock_successful_pollinations_response)
@patch('generator.views.requests.post', return_value=Mock(status_code=500, content=b'API Down'))
def test_generation_fallback_success_fixed(mock_post, mock_get, client):
    """TC-GEN-02: Test de bascule (fallback) : API 1 echec (POST), API 2 succes (GET)"""
    
    prompt_data = {
        'prompt': 'A prompt to test fallback',
        'style': 'Test Style'
    }
    
    response = client.post(reverse('generate_image'), data=prompt_data)
    
    # Vérifications
    assert mock_post.called, "HuggingFace API should have been called"
    assert mock_get.called, "Pollinations API should have been called as fallback"
    
    # Vérifier que la réponse est réussie
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    # Vérifier le contexte
    assert hasattr(response, 'context') and response.context is not None, "No context in response"
    
    # Le fallback devrait avoir fonctionné, donc nous devrions avoir image_data
    assert 'image_data' in response.context, f"Expected 'image_data' in context, got: {list(response.context.keys())}"
    assert len(response.context['image_data']) > 50, f"Image data too short: {len(response.context['image_data'])}"


# Test supplémentaire pour vérifier le cas où les deux APIs échouent
@patch('generator.views.requests.get', return_value=Mock(status_code=200, content=b'small'))  # Contenu trop petit
@patch('generator.views.requests.post', return_value=Mock(status_code=500, content=b'API Down'))
def test_generation_all_apis_fail(mock_post, mock_get, client):
    """TC-GEN-03: Test quand toutes les APIs échouent"""
    
    prompt_data = {
        'prompt': 'A prompt that will fail everywhere',
        'style': 'Failing Style'
    }
    
    response = client.post(reverse('generate_image'), data=prompt_data)
    
    assert response.status_code == 200
    assert 'error' in response.context
    # Le message d'erreur peut varier, testons simplement qu'il y a une erreur
    assert response.context['error'] is not None