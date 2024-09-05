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
from django.urls import include
from django.contrib import admin
from django.urls import path
from main.views import IsLoggedInView, LoginView, SignUpView, TasksView, SubtasksView, AssignedContactView, ContactsView
from add_task.views import CategoriesView, SaveCreatedTaskView, SaveCreatedCategoryView, DeleteCategoryView
from contacts.views import SaveCreatedContactView, SaveChangedContactView, DeleteContactView
from board.views import DeleteTaskView, SaveTaskCategoryView, SaveEditedTaskView

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('isLoggedIn/', IsLoggedInView.as_view()),
    path('login/', LoginView.as_view()),
    path('signUp/', SignUpView.as_view()),
    #path('logout/', LogoutView.as_view()),
    #path('resetPassword/', PasswordResetView.as_view(), name="password_reset"),
    #path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),
    #path('', SignUpView.as_view()),
    path('tasks/', TasksView.as_view()),
    path('subtasks/', SubtasksView.as_view()),
    path('assignedTo/', AssignedContactView.as_view()),
    path('categories/', CategoriesView.as_view()),
    path('contacts/', ContactsView.as_view()),
    path('saveTaskCategory/', SaveTaskCategoryView.as_view()),
    path('saveCreatedTask/', SaveCreatedTaskView.as_view()),
    path('saveEditedTask/', SaveEditedTaskView.as_view()),
    path('saveCreatedContact/', SaveCreatedContactView.as_view()),
    path('saveEditedContact/', SaveChangedContactView.as_view()),
    path('deleteContact/', DeleteContactView.as_view()),    
    path('saveCreatedCategory/', SaveCreatedCategoryView.as_view()),   
    path('deleteCategory/', DeleteCategoryView.as_view()),
    path('deleteTask/', DeleteTaskView.as_view()),   
]
