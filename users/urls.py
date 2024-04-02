from django.conf.urls.static import static
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from config import settings
from users.views import RegisterView, ProfileView, LogoutView, GetMyProfile

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', GetMyProfile.as_view(), name='get_my_profile'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verify/', TokenVerifyView.as_view(), name='token_verify'),
]