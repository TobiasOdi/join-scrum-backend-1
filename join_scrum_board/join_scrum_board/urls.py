"""
URL configuration for join_scrum_board project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from main.views import DataView
""" from add_task.views import SaveCreatedTaskView, SaveCreatedCategoryView, DeleteCategoryView
from contacts.views import SaveCreatedContactView, SaveChangedContactView, DeleteContactView
from board.views import DeleteTaskView, SaveTaskCategoryView, SaveEditedTaskView
 """
urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('user/', include('main.urls')),    
    path('data/', DataView.as_view()),
    path('data/set_categories/', DataView.as_view()),
    path('tasks/', include('add_task.urls')),
    path('contacts/', include('contacts.urls')),
]

"""     
    path('user/login/', LoginView.as_view()),
    path('user/sign_up/', SignUpView.as_view()),
    path('user/reset_password/', PasswordResetView.as_view()),
    path('user/set_new_password/', SetNewPasswordView.as_view()),
    path('user/get_timestamp/<user_id>/', GetTimestampView.as_view()),
    path('user/set_timestamp/', SetTimestampView.as_view()),
    path('tasks/save_task_category/<task_id>/', SaveTaskCategoryView.as_view()),
    path('tasks/save_created_category/', SaveCreatedCategoryView.as_view()),   
    path('tasks/delete_category/<category_id>/', DeleteCategoryView.as_view()),
    path('tasks/save_created_task/', SaveCreatedTaskView.as_view()),
    path('tasks/save_edited_task/<task_id>/', SaveEditedTaskView.as_view()),
    path('tasks/delete_task/<task_id>/', DeleteTaskView.as_view()),
    path('contacts/save_created_contact/', SaveCreatedContactView.as_view()),
    path('contacts/save_edited_contact/', SaveChangedContactView.as_view()),
    path('contacts/delete_contact/', DeleteContactView.as_view())

 """ 
