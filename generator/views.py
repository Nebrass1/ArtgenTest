import base64
import io
import os
import uuid
import urllib.parse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.base import ContentFile
from PIL import Image
import requests
from dotenv import load_dotenv
from artwork.models import Artwork
from category.models import Category

# Template constants
GENERATE_IMAGE_TEMPLATE = 'generate_image.html'

# Charger les variables d'environnement
load_dotenv()

# Importer les secrets depuis le fichier local
try:
    from secrets import HUGGINGFACE_TOKEN
except ImportError:
    HUGGINGFACE_TOKEN = os.getenv("HF_TOKEN", "")

# Configuration API
# FLUX.1-schnell : Modèle rapide et de haute qualité pour la génération d'images
API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
HF_TOKEN = HUGGINGFACE_TOKEN


def query_huggingface(payload):
    """Try HuggingFace API first"""
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        print("HuggingFace Status Code:", response.status_code)

        if response.status_code == 200:
            return response.content
        if response.status_code == 402:
            # Credit limit reached
            raise ValueError("HuggingFace credits exhausted")
        if response.status_code == 503:
            raise RuntimeError("Model loading")
        raise ConnectionError(f"HuggingFace error: {response.status_code}")

    except Exception as e:
        print(f"HuggingFace failed: {e}")
        raise


def query_pollinations(prompt):
    """Fallback to free Pollinations.ai service"""
    try:
        # Pollinations.ai - Free AI image generation
        base_url = "https://image.pollinations.ai/prompt/"
        encoded_prompt = urllib.parse.quote(prompt)
        params = "?width=800&height=800&model=flux&enhance=true"
        full_url = f"{base_url}{encoded_prompt}{params}"

        print(f"Trying Pollinations.ai: {full_url[:100]}...")
        response = requests.get(full_url, timeout=60)

        if response.status_code == 200:
            print(f"✅ Pollinations.ai success: {len(response.content)} bytes")
            return response.content
        raise ConnectionError(f"Pollinations error: {response.status_code}")

    except Exception as e:
        print(f"Pollinations.ai failed: {e}")
        raise


def query(payload):
    """Generate image with fallback system: HuggingFace -> Pollinations.ai"""
    prompt = payload.get("inputs", "")

    # Try HuggingFace first
    try:
        return query_huggingface(payload)
    except Exception as hf_error:
        print(f"HuggingFace failed: {hf_error}")

        # Try Pollinations.ai as fallback
        try:
            return query_pollinations(prompt)
        except Exception as pol_error:
            print(f"Pollinations.ai failed: {pol_error}")

            # If all services fail
            raise RuntimeError(
                "🚫 All AI image services are temporarily unavailable. Please try again later."
            ) from pol_error


def _create_full_prompt(prompt, style):
    """Create the complete prompt for image generation"""
    return f"{prompt}, {style} style, high quality, detailed, masterpiece"


def _validate_and_process_image(image_bytes):
    """Validate and process the generated image"""
    if len(image_bytes) < 100:
        raise ValueError("Invalid image data received")
    
    image = Image.open(io.BytesIO(image_bytes))
    
    # Validate image dimensions
    if image.size[0] < 100 or image.size[1] < 100:
        raise ValueError("Generated image is too small")
    
    # Ensure image is in RGB mode for PNG conversion
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    return image


def generate_image(request):
    """Generate AI artwork - PROTECTED BY CSRF"""
    if request.method != 'POST':
        return render(request, 'generator/index.html')
    
    prompt = request.POST.get('prompt')
    style = request.POST.get('style')
    
    if not (prompt and style):
        return render(request, GENERATE_IMAGE_TEMPLATE, {
            'error': 'Both prompt and style are required'
        })
    
    try:
        # Créer le prompt complet et générer l'image
        full_prompt = _create_full_prompt(prompt, style)
        image_bytes = query({"inputs": full_prompt})
        
        # Valider et traiter l'image
        image = _validate_and_process_image(image_bytes)

        # Convert the image to a format that can be rendered in the template
        img_io = io.BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)
        image_data = base64.b64encode(img_io.read()).decode('utf-8')

        # Render the result template with the image
        categories = Category.objects.all()
        return render(request, 'result.html', {
            'prompt': prompt,
            'style': style,
            'image_data': image_data,
            'categories': categories,
        })
        
    except (ValueError, RuntimeError, ConnectionError) as e:
        error_message = str(e)
        print(f"Image generation error: {error_message}")
        return render(request, GENERATE_IMAGE_TEMPLATE, {
            'error': error_message,
        })

    return render(request, GENERATE_IMAGE_TEMPLATE)


@login_required
def save_generated_artwork(request):
    """Save the generated artwork to the database"""
    if request.method == 'POST':
        try:
            # Get form data
            image_data = request.POST.get('image_data')
            prompt = request.POST.get('prompt')
            style = request.POST.get('style', '')
            category_id = request.POST.get('category_id')

            if not image_data or not prompt:
                messages.error(request, "Missing data to save the artwork.")
                return redirect('generate_image')

            # Decode base64 image
            image_bytes = base64.b64decode(image_data)

            # Validate the decoded image
            if len(image_bytes) < 100:
                messages.error(request, "Invalid image data. Please generate a new image.")
                return redirect('generate_image')

            # Create a unique filename
            filename = f"ai_generated_{uuid.uuid4()}.png"

            # Get or create a default category for AI-generated artworks
            if category_id:
                category = Category.objects.get(id=category_id)
            else:
                category, _ = Category.objects.get_or_create(
                    name="AI Generated",
                    defaults={'description': "Artworks generated by artificial intelligence"}
                )

            # Create the artwork
            artwork = Artwork(
                title=f"AI: {prompt[:50]}",  # Limit title to 50 characters
                description=f"Generated by AI with prompt: {prompt}\nStyle: {style}",
                category=category,
                user=request.user,
                tags=f"ai-generated,{style},{prompt}"
            )

            # Save the image file
            artwork.file.save(filename, ContentFile(image_bytes), save=True)

            messages.success(request, "🎨 Artwork saved successfully!")
            return redirect('artwork_list')

        except (ValueError, RuntimeError, ConnectionError, Category.DoesNotExist) as e:
            error_msg = f"Error during saving: {str(e)}"
            print(error_msg)
            messages.error(request, error_msg)
            return redirect('generate_image')

    return redirect('generate_image')
