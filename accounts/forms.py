# accounts/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile # Assurez-vous que Profile est importé

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]

    # 1. Champs supplémentaires pour User
    first_name = forms.CharField(max_length=30, required=True, help_text='First Name')
    last_name = forms.CharField(max_length=30, required=True, help_text='Last Name')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    
    # 2. Champs pour le Profile
    cin = forms.CharField(max_length=20, required=True, help_text='CIN')
    birthdate = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}), help_text='Birthdate')
    profile_image = forms.ImageField(required=False, help_text='🖼️ Upload your profile picture (optional).')
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, help_text='Select User Role')
    
    # 3. Champs pour la génération de bio par IA
    art_style = forms.CharField(
        max_length=200, 
        required=False,
        help_text='🎨 Your artistic style (ex: Abstract, Realistic, Digital Art, Photography...)',
        widget=forms.TextInput(attrs={'placeholder': 'Ex: Abstract painting, futuristic digital art...'})
    )
    art_interests = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'nature, couleurs, émotions...'}),
        required=False,
        help_text='Your artistic interests (keywords separated by commas).'
    )
    generate_bio = forms.BooleanField(
        required=False,
        initial=True,
        label="Générer ma bio de profil avec l'IA"
    )

    # ====================================================================
    # 🐛 CORRECTION TC-AUTH-02: VALIDER L'UNICITÉ DE L'EMAIL
    # ====================================================================
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Vérifie si l'email existe déjà (la recherche est insensible à la casse)
        # On ne doit pas bloquer la vérification si l'email est None, mais il est 'required'.
        if email and User.objects.filter(email__iexact=email).exists():
            # Déclenche l'erreur qui empêchera la création de l'utilisateur
            raise forms.ValidationError("Cette adresse e-mail est déjà utilisée par un autre compte.")
            
        return email
    # ====================================================================
    
    class Meta:
        model = User
        # On utilise les champs par défaut de UserCreationForm + tous les champs personnalisés
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'cin', 'birthdate', 'role', 'art_style', 'art_interests', 'profile_image', 'generate_bio')
        
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'birthdate': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Birthdate'}),
            'profile_image': forms.ClearableFileInput(attrs={'placeholder': 'Profile Picture'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        # Grant admin access if the role is admin
        if self.cleaned_data['role'] == 'admin':
            user.is_staff = True
            user.is_superuser = True  # This grants full access to the admin interface

        if commit:
            user.save()
            
            # Get or create the profile (created automatically par un signal, sinon utiliser Profile.objects.create)
            profile = user.profile
            
            # Update profile fields
            profile.cin = self.cleaned_data['cin']
            profile.birthdate = self.cleaned_data['birthdate']
            profile.role = self.cleaned_data['role']
            profile.art_style = self.cleaned_data.get('art_style', '')
            profile.art_interests = self.cleaned_data.get('art_interests', '')
            
            # Handle photo separately (IMPORTANT for files)
            profile_image = self.cleaned_data.get('profile_image')
            if profile_image:
                profile.photo = profile_image
                
            profile.save() # Sauvegarde du profil

        return user