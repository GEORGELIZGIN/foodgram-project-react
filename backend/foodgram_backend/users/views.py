from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import pagination, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Subscription
from .serializers import SubscriptionSerializer

User = get_user_model()


class SubscriptionViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    pagination_class = pagination.LimitOffsetPagination
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        self.request.user
        return User.objects.filter(
            id__in=self.request.user.followings.all().values_list(
                'author__id', flat=True))


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def create_delete_subscription(request, id):
    user = User.objects.filter(id=id).first()
    if not user:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.user == user:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    subscription = Subscription.objects.filter(
        follower=request.user, author=user
    ).first()
    if request.method == 'POST':
        if subscription:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        Subscription.objects.create(follower=request.user, author=user)
        return HttpResponse(status=status.HTTP_201_CREATED)
    if not subscription:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    subscription.delete()
    return HttpResponse(status=status.HTTP_204_NO_CONTENT)
