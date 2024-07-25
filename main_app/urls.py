from django.urls import path
from . import views
urlpatterns=[
    path("home.html/",views.home,name="home"),
    path("register.html/",views.register,name="register"),   
    path("",views.sign,name="sign"),  
    path("result.html/",views.result,name="sign"),
    path("history.html/",views.history,name="sign"),
    path("hyper.html/",views.hyper,name="hyper"),
    path('upload/', views.upload_image_view, name='upload_image_view'),
    path('delete_item/<item_id>', views.delete_item, name='delete-item'),   
]