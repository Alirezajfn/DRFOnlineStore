from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.api.urls', namespace='users'), name='users'),
    path('api/authenticate/', include('authentications.api.urls', namespace='authentications'),
         name='authentications'),
    path('api/category/', include('category.api.urls', namespace='category'), name='category'),
    path('api/product/', include('product.api.urls', namespace='product'), name='product'),
    path('api/permission/', include('permissions.api.urls', namespace='permission'), name='permission'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularSwaggerView.as_view(url_name='schema'), name='redoc'),

]
