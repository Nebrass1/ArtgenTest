from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Subcategory
from .forms import CategoryForm, SubcategoryForm
from .serializers import SubcategorySerializer
from django.conf import settings
import requests
import os
from dotenv import load_dotenv
from requests import post, exceptions
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import google.generativeai as genai

# Template constants
SUBCATEGORY_FORM_TEMPLATE = 'subcategory_form.html'

# Charger les variables d'environnement
load_dotenv()


@login_required
def category_list(request):
    """List all categories"""
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


def category_create(request):
    """Create a new category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('category-list')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form})


def category_update(request, pk):
    """Update an existing category"""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category-list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_form.html', {'form': form})


def category_delete(request, pk):
    """Delete a category"""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category-list')
    return render(request, 'category_delete.html', {'category': category})


@login_required
def subcategory_list_view(request, category_id):
    """List subcategories for a category with AI generation"""
    category = get_object_or_404(Category, id=category_id)
    subcategories = Subcategory.objects.filter(category=category)

    if request.method == 'POST':
        try:
            generated_subcategories = generate_subcategories(category.name)
            for name in generated_subcategories:
                Subcategory.objects.get_or_create(name=name, category=category)
            subcategories = Subcategory.objects.filter(category=category)
        except exceptions.RequestException as e:
            error_message = f"Error generating subcategories: {str(e)}"
    
    error_message = ''
    return render(request, 'subcategory_list.html', {
        'category': category,
        'subcategories': subcategories,
        'error_message': error_message if error_message else None,
    })


def generate_subcategories(category_name):
    """Generate subcategories using external API"""
    url = "https://gemini.googleapis.com/v1/models/gemini-pro:generateContent"
    headers = {
        "Authorization": f"Bearer {settings.GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": f"Generate subcategories for the category '{category_name}'.",
        "max_tokens": 50
    }

    response = post(url, headers=headers, json=payload)
    print(response)
    response.raise_for_status()

    subcategories = response.json().get('subcategories', [])
    return [subcategory.strip() for subcategory in subcategories]


def subcategory_list(request, category_id):
    """List all subcategories for a specific category"""
    category = get_object_or_404(Category, id=category_id)
    subcategories = Subcategory.objects.filter(category=category)
    return render(request, 'subcategory_list.html', {
        'category': category,
        'subcategories': subcategories,
    })


@csrf_exempt
def subcategory_create(request, category_id):
    """Create a new subcategory (AJAX or form)"""
    category = get_object_or_404(Category, id=category_id)
    
    if request.method != 'POST':
        form = SubcategoryForm()
        return render(request, SUBCATEGORY_FORM_TEMPLATE, {'form': form, 'category': category})
    
    if _is_ajax_request(request):
        return _handle_ajax_subcategory_creation(request, category)
    
    result = _handle_form_subcategory_creation(request, category)
    if result:
        return result
    
    form = SubcategoryForm(request.POST)
    return render(request, SUBCATEGORY_FORM_TEMPLATE, {'form': form, 'category': category})


def subcategory_update(request, category_id, pk):
    """Update a subcategory"""
    category = get_object_or_404(Category, id=category_id)
    subcategory = get_object_or_404(Subcategory, pk=pk)
    
    if request.method == 'POST':
        form = SubcategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
            return redirect('subcategory-list', category_id=category.id)
    else:
        form = SubcategoryForm(instance=subcategory)
    
    return render(request, SUBCATEGORY_FORM_TEMPLATE, {'form': form, 'category': category})


def subcategory_delete(request, category_id, pk):
    """Delete a subcategory"""
    category = get_object_or_404(Category, id=category_id)
    subcategory = get_object_or_404(Subcategory, pk=pk)
    
    if request.method == 'POST':
        subcategory.delete()
        return redirect('subcategory-list', category_id=category.id)
    
    return render(request, 'subcategory_delete.html', {'subcategory': subcategory, 'category': category})


def _handle_ajax_subcategory_creation(request, category):
    """Handle AJAX subcategory creation"""
    name = request.POST.get('name')
    description = request.POST.get('description', '')
    
    if not name:
        return JsonResponse({'success': False, 'error': 'Name is required'}, status=400)
    
    try:
        subcategory = Subcategory.objects.create(
            name=name,
            description=description,
            category=category
        )
        return JsonResponse({
            'success': True,
            'message': 'Subcategory added successfully',
            'subcategory': {
                'id': subcategory.id,
                'name': subcategory.name,
                'description': subcategory.description
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def _is_ajax_request(request):
    """Check if request is AJAX"""
    return (request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 
            'application/json' in request.headers.get('Accept', ''))


def _handle_form_subcategory_creation(request, category):
    """Handle form subcategory creation"""
    form = SubcategoryForm(request.POST)
    if form.is_valid():
        subcategory = form.save(commit=False)
        subcategory.category = category
        subcategory.save()
        return redirect('subcategory-list', category_id=category.id)
    return None


def _configure_gemini_api():
    """Configure Gemini API and return model instance"""
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        raise ValueError('API key not configured')
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-flash-latest')


def _create_subcategory_prompt(category_name):
    """Create the prompt for Gemini API"""
    return f"""List exactly 5 subcategories for the artistic category '{category_name}'.
For each subcategory, provide the name and a brief description on the same line.
Strict format (one per line):
Subcategory Name: Short description

Example:
Portraits: Artistic representations of people
Landscapes: Natural or urban scenes

Now generate the 5 subcategories for '{category_name}'."""


def _parse_subcategory_response(response_text, category_name):
    """Parse Gemini response to extract subcategories"""
    subcategories = []
    lines = response_text.split('\n')
    
    for line in lines:
        line = line.strip()
        
        if _should_skip_line(line):
            continue
            
        parsed = _parse_subcategory_line(line)
        if parsed:
            subcategories.append(parsed)
            
            if len(subcategories) >= 5:
                break
    
    if not subcategories:
        return [{
            'subcategory': f'Unparsed response for {category_name}',
            'description': response_text[:200]
        }]
    
    return subcategories


def _should_skip_line(line):
    """Determine if a line should be skipped during parsing"""
    if not line or line.startswith('#'):
        return True
    
    skip_keywords = ['voici', 'exemple']
    return any(line.lower().startswith(keyword) for keyword in skip_keywords)


def _parse_subcategory_line(line):
    """Parse a line to extract subcategory and description"""
    line = line.lstrip('0123456789.*- ')
    
    if ':' not in line:
        return None
    
    parts = line.split(':', 1)
    subcategory = parts[0].strip().replace('**', '').replace('*', '').strip()
    description = parts[1].strip() if len(parts) > 1 else ''
    
    if subcategory and len(subcategory) < 100 and description:
        return {
            'subcategory': subcategory,
            'description': description
        }
    return None


@csrf_exempt
def get_art_subcategories(request, category_id):
    """Generate subcategories using Gemini AI API"""
    try:
        subcategories = _generate_subcategories_with_gemini(category_id)
        return JsonResponse({'subcategories': subcategories})
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)
    except Exception as e:
        print(f"Error in get_art_subcategories: {str(e)}")
        return JsonResponse({'error': f'Internal server error: {str(e)}'}, status=500)


def _generate_subcategories_with_gemini(category_id):
    """Generate subcategories using Gemini AI"""
    model = _configure_gemini_api()
    category = Category.objects.get(id=category_id)
    
    prompt = _create_subcategory_prompt(category.name)
    response = model.generate_content(prompt)
    print("Gemini Response:", response.text)
    
    return _parse_subcategory_response(response.text, category.name)