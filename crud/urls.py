from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('gender/list', views.gender_list),
    path('gender/add', views.add_gender),
    path('gender/edit/<int:genderId>',views.edit_gender),
    path('gender/delete/<int:genderId>',views.delete_gender),
    path('user/list', views.user_list),
    path('user/edit/<int:userId>', views.edit_user),
    path('user/delete/<int:userId>', views.delete_user),
    path('user/add', views.add_user)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
