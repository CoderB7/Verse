from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('dashboard/channels/', views.ChannelListView.as_view(), name='dashboard-channels'),
    path('dashboard/channels/<int:channel_id>/posts/', views.PostListView.as_view(), name='post-list'),
    path('dashboard/channels/<int:channel_id>/post/', views.PostCreateView.as_view(), name='post-create'),
    path('dashboard/channels/<int:channel_id>/post/<int:post_id>/', views.PostUpdateView.as_view(), name='post-update'),
    
    path('dashboard/blogs/', views.BlogListView.as_view(), name='dashboard-blogs'),
    path('dashboard/blogs/<int:blog_id>/posts/', views.PostListView.as_view(), name='blog-post-list'),
    path('dashboard/blogs/<int:blog_id>/post/', views.PostCreateView.as_view(), name='blog-post-create'),

    path('user_info/', views.get_user_info, name='user_info'),
    
    # path('add_chat/', views.add_chat_info, name='add_chat'),
    # path('close/', views.delete_webhook, name='delete_webhook'),   
]

