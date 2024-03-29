"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_content.urls')),
    path('accounts/', include('app_accounts.urls')),
    path('workshop/', include('app_workshop.urls')),
    path('mycourses/', include('app_mycourses.urls')),
    path('cart/', include('app_cart.urls')),
    path('contacts/', include('app_contacts.urls')),
    path('reviews/', include('app_reviews.urls')),
    path('tutorial/', include('app_tutorial.urls')),
    path('service/', include('app_service.urls')),
    # path('stripe/', include('app_stripe.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
