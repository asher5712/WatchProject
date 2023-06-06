from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Utilizing routers for routing the urls
router = DefaultRouter()
router.register('stream', views.StreamPlatformView, basename='streamplatform')

# Default url configrations
urlpatterns = [
    # Routes for watch item
    path('list', views.WatchListAV.as_view(), name='watch-list'),
    path('<int:pk>', views.WatchListDetailAV.as_view(), name='watch-details'),
    
    # Routes for reviewing the movie
    path('<int:pk>/reviews', views.ReviewList.as_view(), name='review-list'),
    path('<int:pk>/review-create', views.ReviewCreate.as_view(), name='review-create'),
    path('review/<int:pk>', views.ReviewDetail.as_view(), name='review-details'),
    
    path('', include(router.urls)), # Including routers in default routes
    
    # path('platform', views.PlatformListAV.as_view(), name='platform-list'),
    # path('platform/<int:pk>', views.PlatformDetailAV.as_view(), name='platform-details'),
    
]