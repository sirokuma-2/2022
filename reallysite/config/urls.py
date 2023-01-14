from django.contrib import admin
from django.urls import path,include
from django.views.decorators.cache import cache_page

from django.contrib.sitemaps.views import sitemap
from config.sitemaps import StaticViewSitemap,BlogSitemap

sitemaps = {
    "static":StaticViewSitemap,
    "blog":BlogSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path('blog/',include('blog.urls')),
    path('',include('mysite.urls')),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')
]