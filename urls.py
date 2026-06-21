from django.contrib import admin
from django.urls import path
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# LogMessageView ko bhi import list mein add kar diya hai
from api.views import DialNumberView, LogMessageView, home_frontend

schema_view = get_schema_view(
   openapi.Info(
      title="International Contact Dialing API",
      default_version='v1',
      description="Semester Project API validating dialing structures for specific countries.",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Main Frontend Template Route
    path('', home_frontend, name='frontend_home'), 
    
    path('admin/', admin.site.urls),
    path('api/login/', obtain_auth_token, name='api_token_auth'),
    
    # Endpoints for Database logging & validation
    path('api/dial/', DialNumberView.as_view(), name='dial-number'),
    path('api/log-message/', LogMessageView.as_view(), name='log-message'), # <-- Naya Message Endpoint
    
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]