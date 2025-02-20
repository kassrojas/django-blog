# blog/urls.py
from django.urls import path, include
from .views import Index, BlogDetailsView, LikeBlogPost, Featured, DeletePostView

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('<int:pk>/', BlogDetailsView.as_view(), name='blog_details'),
    path('tinymce/', include('tinymce.urls')),
    path('<int:pk>/like', LikeBlogPost.as_view(), name='like_post'),
    path('featured/', Featured.as_view(), name='featured'),
    path('<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
]