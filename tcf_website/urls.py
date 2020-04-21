"""Routes URLs to views"""

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.AboutView.as_view(), name='about'),
    path('privacy', views.privacy, name='privacy'),
    path('terms', views.terms, name='terms'),
    path('browse', views.browse, name='browse'),
    path('department/<int:dept_id>', views.department, name='department'),
    path('course/<int:course_id>', views.course_view, name='course'),
    path('course/<int:course_id>/<int:instructor_id>',
         views.course_instructor, name='course_instructor'),
    path('reviews/new', views.new_review, name='new_review'),
    path('reviews', views.reviews, name='reviews'),
    path('reviews/<int:review_id>/upvote', views.upvote),
    path('reviews/<int:review_id>/downvote', views.downvote),
    path('profile', views.profile, name='profile'),


    # AUTH URLS
    path('accounts/profile/', views.browse),
    path('login', views.login, name='login'),
    path('login/error', views.login_error),
    path('login/collect_extra_info', views.collect_extra_info),
    path('accounts/login/', views.login),
    path('logout/', views.logout, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
