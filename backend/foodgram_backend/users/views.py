from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from rest_framework import pagination, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import Subscription
from users.serializers import SubscriptionSerializer

User = get_user_model()

CONTENT_TYPE = 'application/json'

class CustomPaginator(pagination.PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'limit'


class SubscriptionViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPaginator
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
        subscription = Subscription.objects.create(
            follower=request.user, author=user)
        serializer = SubscriptionSerializer(user, context={'request': request})
        return JsonResponse(
            serializer.data,
            content_type=CONTENT_TYPE,
            status=status.HTTP_201_CREATED,
        )
    if not subscription:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    subscription.delete()
    return HttpResponse(status=status.HTTP_204_NO_CONTENT)
