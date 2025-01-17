from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500, handler400
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('app.urls')),
    path('compiler/', include('compiler.urls')),
    path('auth/', include('accounts.urls')),
    path('programs/', include('course.urls')),
    path('result/', include('result.urls')),
    path('search/', include('search.urls')),
    path('quiz/', include('quiz.urls')),
    path('blog/', include('blog.urls')),
    path('records/', include('student_record.urls')),
    path('tinymce/', include('tinymce.urls')),

    #intergrading the restful APIS
    path('api/', include('accounts.api.urls', namespace='accounts-api')),  # Include the "accounts" app's URLs here
    path('api/', include('course.api.urls', namespace='courses-api')),  # Include your app's API URLs here
    path('api/', include('app.api.urls', namespace='dashboard-api')),

    #admin functionality
    path('kreeckdevsadmin/doc/', include('django.contrib.admindocs.urls')), #this will show the docs in the admin pan
    path('kreeckdevsadmin/', admin.site.urls),

    #payments
    path('payments/', include('payments.urls')),

    # Support, Enable this only in Production
    #path('support/', include('support.urls')),
    #path("__reload__/", include("django_browser_reload.urls")),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG == False:
    handler404 = 'app.views.handler404'
    handler500 = 'app.views.handler500'
    handler400 = 'app.views.handler400'
else:
    pass

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]