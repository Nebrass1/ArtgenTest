# accounts/views.py
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .forms import CustomUserCreationForm
from .bio_generator import get_bio_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import os

def register(request):
    """Vue d'inscription d'utilisateur simplifiée"""
    if request.method != 'POST':
        form = CustomUserCreationForm()
        return render(request, 'accounts/register.html', {'form': form})
    
    form = CustomUserCreationForm(request.POST, request.FILES)
    if not form.is_valid():
        return render(request, 'accounts/register.html', {'form': form})
    
    # Récupérer les données du formulaire
    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password1')
    
    # Sauvegarder l'utilisateur
    user = form.save()
    
    # Authentifier et connecter l'utilisateur
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        messages.success(request, '✅ Registration successful! Welcome to ArtiGen.')
        return redirect('profile')
    
    # En cas d'échec d'authentification (rare)
    messages.success(request, '✅ Registration successful! Please log in.')
    return redirect('login')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Check if the user has the 'admin' role and redirect accordingly
            if user.profile.role == 'admin':
                return redirect('/admin/')  # Redirect to Django's admin interface
            else:
                return redirect('profile')  # Redirect to profile for regular users
        else:
            messages.error(request, 'Invalid username or password.')  # Show error message
    return render(request, 'accounts/login.html')

@login_required
def profile(request):
    from artwork.models import ArtCollection
    from blog.models import Post, Favourites
    
    profile_photo = request.user.profile.photo.url if request.user.profile.photo else None
    
    # Calculate user statistics
    galleries_count = ArtCollection.objects.filter(user=request.user).count()
    posts_count = Post.objects.filter(author=request.user).count()
    favorites_count = Favourites.objects.filter(user=request.user).count()
    
    return render(request, 'accounts/profile.html', {
        'username': request.user.username,
        'user': request.user,
        'profile_photo': profile_photo,
        'join_date': request.user.date_joined.strftime('%B %d, %Y'),
        'PROFILE_PHOTOS_URL': settings.PROFILE_PHOTOS_URL,
        'galleries_count': galleries_count,
        'posts_count': posts_count,
        'favorites_count': favorites_count
    })

def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
@require_http_methods(["POST"])
def generate_bio_ajax(request):
    """
    Generate or regenerate profile bio via AJAX
    """
    try:
        art_style = request.POST.get('art_style', '')
        art_interests = request.POST.get('art_interests', '')
        tone = request.POST.get('tone', 'professional')
        
        if not art_style and not art_interests:
            return JsonResponse({
                'success': False,
                'error': 'Please provide at least your art style or interests.'
            })
        
        # Generate the bio
        bio_generator = get_bio_generator()
        result = bio_generator.generate_bio(
            username=request.user.username,
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            art_style=art_style,
            art_interests=art_interests,
            tone=tone
        )
        
        if result['success']:
            # Save to profile
            profile = request.user.profile
            profile.bio = result['bio']
            profile.art_style = art_style
            profile.art_interests = art_interests
            profile.bio_generated = True
            profile.save()
            
            return JsonResponse({
                'success': True,
                'bio': result['bio'],
                'message': '✨ Your bio has been generated successfully!'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': result.get('error', 'Unknown error during generation')
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Server error: {str(e)}'
        })


@login_required
def edit_profile(request):
    """
    Profile editing page with bio generation
    """
    profile = request.user.profile
    
    if request.method == 'POST':
        # Manual profile update
        profile.bio = request.POST.get('bio', profile.bio)
        profile.art_style = request.POST.get('art_style', profile.art_style)
        profile.art_interests = request.POST.get('art_interests', profile.art_interests)
        
        # Profile photo
        if 'photo' in request.FILES:
            profile.photo = request.FILES['photo']
        
        profile.save()
        messages.success(request, '✅ Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'accounts/edit_profile.html', {
        'profile': profile,
        'user': request.user
    })
