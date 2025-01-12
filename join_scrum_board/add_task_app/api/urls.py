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
from django.urls import path
from add_task_app.api.views import SaveCreatedTaskView, SaveCreatedCategoryView, DeleteCategoryView

urlpatterns = [
    path('save_created_category/', SaveCreatedCategoryView.as_view()),   
    path('delete_category/<int:category_id>/', DeleteCategoryView.as_view()),
    path('save_created_task/', SaveCreatedTaskView.as_view()),
]