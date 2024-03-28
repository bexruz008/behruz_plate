from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

schema_view = get_schema_view(
   openapi.Info(
      title="behruz drf",
      default_version='v1',
      description="Template for DRF",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="behruzabduqodirov17@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   # permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', include('app.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('api-token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/token/verfiy', TokenVerifyView.as_view(), name='token-verify')
]