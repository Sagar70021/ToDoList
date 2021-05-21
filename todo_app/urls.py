from django.urls import path
from todo_app import views
from django.contrib.auth.views import LogoutView

app_name = 'todo_app'

urlpatterns=[
    path('login/',views.CustomLoginView.as_view(),name='login'),
    path('register/',views.Registerpage.as_view(),name='register'),
    path('logout/',views.LogoutView.as_view(next_page='todo_app:login'),name='logout'),
    path('',views.TaskList.as_view(),name='list'),
    path('<int:pk>/',views.TaskDetail.as_view(),name='detail'),
    path('create/',views.TaskCreate.as_view(),name='create'),
    path('update/<int:pk>/',views.TaskUpdate.as_view(),name='update'),
    path('delete/<int:pk>/',views.TaskDelete.as_view(),name='delete'),


]
