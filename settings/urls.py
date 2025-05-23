from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from django.conf.urls.i18n import i18n_patterns # Mutlilingual

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

from grapple import urls as grapple_urls

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("accounts/", include("allauth.urls")),
    path("api/", include(grapple_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns += debug_toolbar_urls()


urlpatterns += i18n_patterns(
    path('search/', search_views.search, name='search'),
    path("eliasells/", include("eliasells.urls")),  # Add this to include home app's URLs
    path("", include(wagtail_urls)),
)
