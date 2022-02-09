from django.urls import path

from . import views

urlpatterns = [
    path(
        'users/subscriptions/',
        views.SubscriptionViewSet.as_view({'get': 'list'},)),
    path('users/<int:id>/subscribe/', views.create_delete_subscription),
]
