from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:year>/<str:month>/', views.home, name="home"),
    path('events', views.all_events, name="all-events"),
    path('add_venue', views.add_venue, name="add-venue"),
    path('all_posts_list_view', views.AllPostsListView.as_view(), name="all-posts-home-view"),
    path('detail_post_article/<int:pk>', views.ArticleDetailView.as_view(), name="detail-post-article"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
