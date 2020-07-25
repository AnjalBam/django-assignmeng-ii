from django.urls import path
from .views import (HomeView, CreateBlog, BlogDetailView,
                    UpdateBlog, DeleteBlog)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('create/', CreateBlog.as_view(), name='create'),
    path('<slug:slug>/', BlogDetailView.as_view(), name='detail'),
    path('<slug:slug>/update/', UpdateBlog.as_view(), name='update'),
    path('<slug:slug>/delete/', DeleteBlog.as_view(), name='delete'),
]
