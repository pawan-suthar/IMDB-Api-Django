from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.api_root), #entry point
    path('list/', views.movie_list, name="Watchlist-list"),
    path('list/<int:pk>/', views.movie_detail, name="Watchlist-detail"),
    path('stream/', views.stream_list.as_view(), name="Platforms-list"),
    path('stream/<int:pk>/', views.stream_detail.as_view(), name="Platforms-detail"),
    # path('review/', views.Review_list.as_view(), name="review-list"),
    # path('review/<int:pk>', views.Review_detail.as_view(), name="review-detail"),


    # ---------------------- get review for particular movie --------------------- #
    path('list/<int:pk>/review', views.Review_list.as_view(), name="review-list"),
    path('list/<int:pk>/review-create', views.Review_create.as_view(), name="review-create"),
    path('list/review/<int:pk>', views.Review_detail.as_view(), name="review-detail")
]
urlpatterns = format_suffix_patterns(urlpatterns)
