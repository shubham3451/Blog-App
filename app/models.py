from django.db import models
from django.contrib.auth.models import  BaseUserManager, AbstractBaseUser 
from django.core.exceptions import ValidationError
from datetime import date

# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, email,username, password=None):
        """
        Creates and saves a User with the given email, username date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email, username, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)  
    last_active = models.DateTimeField(auto_now=True)  
    date_modified = models.DateTimeField(auto_now=True)  


    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username",]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    

class Profile(models.Model):
    user = models.OneToOneField(MyUser,on_delete=models.CASCADE)
    profile_pic = models.ImageField(blank=True, null=True, upload_to='profile_pic/', default='profile_pic/default_profile_pic.jpeg')
    cover_pic = models.ImageField(blank=True, null=True, upload_to='cover_pic/')
    bio = models.CharField(blank=True, null=True, max_length=500)
    phone = models.CharField(blank=True, null=True, max_length=50)
    date_of_birth = models.DateField(blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(blank=True, null=True,max_length=50)

    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def clean(self):
        if self.date_of_birth:
            today = date.today()
            age = self.date_of_birth.year - today.year
            if today.month < self.date_of_birth.month or (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day):
                age -= 1
            if age < 12:
                raise ValidationError("You must be at least 12 years old.")
        return super().clean()


class Post(models.Model):
    POST_TYPE_CHOICES = (
        ('text', 'Text Post'),  # Text content only
        ('image', 'Image Post'),  # Image content
        ('video', 'Video Post'),  # Video content
        ('audio', 'Audio Post'),  # Audio content
        ('link', 'Link Post'),  # Link content
        ('mixed', 'Mixed Post'),  
    )

    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)  # User who created the post
    content = models.TextField(null=True, blank=True)  # Main text content, like a tweet
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES, default='text')  # Type of post (text, image, etc.)

    # Media fields for optional media content
    image = models.ImageField(upload_to='posts/images/', null=True, blank=True)  # Image upload
    video = models.FileField(upload_to='posts/videos/', null=True, blank=True)  # Video upload
    audio = models.FileField(upload_to='posts/audios/', null=True, blank=True)  # Audio upload
    link = models.URLField(max_length=200, null=True, blank=True)  # External link sharing

    # Timestamps for tracking when the post was created or modified
    date_posted = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:50]  # Display the first 50 characters of the post content

    def save(self, *args, **kwargs):
        # Ensure the correct media for the post type
        if self.post_type == 'image' and not self.image:
            raise ValueError("An image must be provided for an image post.")
        elif self.post_type == 'video' and not self.video:
            raise ValueError("A video file must be provided for a video post.")
        elif self.post_type == 'audio' and not self.audio:
            raise ValueError("An audio file must be provided for an audio post.")
        elif self.post_type == 'link' and not self.link:
            raise ValueError("A URL must be provided for a link post.")
        elif self.post_type == 'mixed' and not (self.image or self.video or self.audio or self.link):
            raise ValueError("A mixed post must contain at least one type of media (image/video/audio/link).")

        super().save(*args, **kwargs)  # Call the parent class's save method





