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
from board_app.api.views import DataView, SetCategoriesView, DeleteTaskView, SaveTaskCategoryView, SaveEditedTaskView, SaveSubtaskStatus

urlpatterns = [
    path('data/', DataView.as_view()),
    path('data/set_categories/', SetCategoriesView.as_view()),
    path('save_task_category/<int:task_id>/', SaveTaskCategoryView.as_view()),
    path('save_edited_task/<int:task_id>/', SaveEditedTaskView.as_view()),
    path('delete_task/<int:task_id>/', DeleteTaskView.as_view()),
    path('save_subtask_status/<int:subtask_id>/', SaveSubtaskStatus.as_view()),
]