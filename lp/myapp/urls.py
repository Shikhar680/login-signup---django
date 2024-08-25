from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('admin/<str:username>/',views.adminis,name="admin"),
    # path('test_message_creation/',views.test_message_creation,name="test_message_creation"),
    # path('post_message/', views.post_message, name='post_message'),
    path('userlist/',views.userlist,name="userlist")
]