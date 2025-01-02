from django import forms
from .models import MyUser, Profile, Post
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from datetime import date
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):

    class Meta:
        model= MyUser
        fields = ('email', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if MyUser.objects.filter(email=email).exists():
            raise forms.ValidationError("email already exists")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if MyUser.objects.filter(username=username).exists():
            raise forms.ValidationError(f"{username} is taken")
        return username
    


class LogInForm(AuthenticationForm):
    username = forms.EmailField(label='Email')  # Change the username field to email

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('username')  # 'username' is replaced by email
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError('Invalid email or password.')
        return cleaned_data

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'bio', 'profile_pic','cover_pic', 'date_of_birth', 'phone',)
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),  # Calendar widget for birth_date
        }



class EditUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['email', 'username']  # Only allow editing email and username.

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Ensure the email is unique
        if MyUser.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Email is already taken. Please choose a different email.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Ensure the username is unique
        if MyUser.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise forms.ValidationError(f"Username '{username}' is already taken. Please choose a different username.")
        return username
    
class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'post_type', 'image', 'video', 'audio', 'link']

    # Add any additional form validation here if necessary
    def clean(self):
        cleaned_data = super().clean()
        post_type = cleaned_data.get('post_type')
        image = cleaned_data.get('image')
        video = cleaned_data.get('video')
        audio = cleaned_data.get('audio')
        link = cleaned_data.get('link')

        # Ensure that the appropriate media is provided based on the post type
        if post_type == 'image' and not image:
            raise forms.ValidationError("An image must be provided for an image post.")
        elif post_type == 'video' and not video:
            raise forms.ValidationError("A video file must be provided for a video post.")
        elif post_type == 'audio' and not audio:
            raise forms.ValidationError("An audio file must be provided for an audio post.")
        elif post_type == 'link' and not link:
            raise forms.ValidationError("A URL must be provided for a link post.")
        elif post_type == 'mixed' and not (image or video or audio or link):
            raise forms.ValidationError("A mixed post must contain at least one type of media (image/video/audio/link).")

        return cleaned_data
    



