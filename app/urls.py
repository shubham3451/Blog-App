from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',view=views.signUp,name='signUp'),
    path('login/',view=views.LogIn,name='logIn'),
    path('logout/',view=views.LogOut,name='logout'),
    path('profile/',view=views.Profile,name='profile'),
    path('profile/<str:username>/', views.Profile, name='profile_with_username'),  # For other users' profiles
    path('update_profile/', view=views.SetUpProfile,name='updateprofile'),
    path('dashboard/', view=views.Dashboard,name='dashboard'),
    path('search_suggestions/', views.search_suggestions, name='search_suggestions'),
    path('create_post/',view=views.CreatePost, name='createpost'),
    path('editpost<int:post_id>/',view=views.EditPost,name='editpost'),
    path('deletepost<int:post_id>/',view=views.deletePost,name='deletepost'),
    path('deleteuser/', view=views.DeleteUser,name='deleteuser'),
    path('changepassword/', view=views.passwordChange, name='changepassword'),
    path('forgot-password/', auth_views.PasswordResetView.as_view(template_name="password_reset_form.html",  email_template_name="password_reset_email.html"), name='password_reset'),
    path('forgot-password/done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name='password_reset_complete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
