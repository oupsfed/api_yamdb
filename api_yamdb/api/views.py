from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.decorators import permission_classes
from rest_framework import viewsets, filters, status, mixins, permissions
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import IsAdmin
from .serializer import UserSerializer, AuthSerializer, TokenSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    def get_object(self):
        if self.kwargs['username'] == 'me':
            print(self.request.path)
            obj = get_object_or_404(User, pk=self.request.user.pk)
            return obj


@api_view(['POST'])
@permission_classes([AllowAny])
def auth(request):
    serializer = AuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']

    if (not User.objects.filter(username=username).exists()
            and User.objects.filter(email=email).exists()):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username, email=email)
        code = default_token_generator.make_token(user)
        send_mail(
            subject='Ваш код аутентификации',
            message='Сохраните код! Он понадобится вам для получения токена.\n'
                    f'confirmation_code:\n{code}\n'
                    f'username: {username}',
            from_email='admn@yamdb.com',
            recipient_list=[email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    if not User.objects.filter(username=username, email=email).exists():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, username=username, email=email)
    code = default_token_generator.make_token(user)
    send_mail(
        subject='Ваш код аутентификации',
        message='Сохраните код! Он понадобится вам для получения токена.\n'
                f'confirmation_code:\n{code}\n'
                f'username: {username}',
        from_email='admn@yamdb.com',
        recipient_list=[email],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, code):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)

    return Response({"message": "неверный код подтверждения."},
                    status.HTTP_400_BAD_REQUEST)
