from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.decorators import permission_classes, action
from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import mixins

from .permissions import IsAdmin, IsAdminOrReadOnly
from .serializers import UserSerializer, AuthSerializer, TokenSerializer
from reviews.models import Category, Genre
from .permissions import UserPermission
from .serializers import CategorySerializer, GenreSerializer
from .serializers import TitleSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    def update(self, request, *args, **kwargs, ):
        if request.method == 'PUT':
            return Response('Метод PUT не разрешен!',
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        user = User.objects.filter(username=kwargs['username']).get()
        serializer = self.serializer_class(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.pop('role', None)
        serializer.update(user, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if (User.objects.filter(email=request.data['email']).exists()
                or User.objects.filter(
                    username=request.data['username']).exists()):
            return Response(
                'Такой email уже существует',
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=['GET', 'PATCH'],
        permission_classes=(IsAuthenticated,),
        detail=False,
        url_path='me',
    )
    def user_info(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.pop('role', None)
        serializer.update(request.user, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


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


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response({'Нельзя смотреть определенные категории'},
                        status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response({'Нельзя смотреть определенные категории'},
                        status.HTTP_405_METHOD_NOT_ALLOWED)
