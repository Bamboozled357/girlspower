import django_filters
from django.shortcuts import render
from django.http import HttpResponse


from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import filters, status, mixins
from rest_framework.generics import (ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView)
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import (Message, Publication, Comment)
from .permissions import IsAuthorOrIsAdmin, IsAuthor
from .serializers import (MessageSerializer, PublicationListSerializer,
                          PublicationSerializer, PublicationDetailSerializer, PublicationLikeSerializer,
                          CommentSerializer)
from django.contrib.auth import get_user_model

User = get_user_model()

# from .tasks import sleepy


# def index(request):
#     sleepy(10)
#     return HttpResponse('<h1>TASK IS DONE!</h1>')


class PublicationListView(ListAPIView):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]


class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('title_only'):
            return ['title']
        return super(CustomSearchFilter, self).get_search_fields(view, request)


class ListPublicationAPIView(ListAPIView):
    permission_classes = [AllowAny, ]

    queryset = Publication.objects.all()
    serializer_class = PublicationListSerializer


class CreatePublicationAPIView(CreateAPIView):

    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    permission_classes = [IsAuthorOrIsAdmin, ]


class DetailPublicationAPIView(RetrieveAPIView):
    permission_classes = [AllowAny, ]
    queryset = Publication.objects.all()
    serializer_class = PublicationDetailSerializer


class UpdatePublicationAPIView(UpdateAPIView):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    permission_classes = [IsAuthorOrIsAdmin, ]


class DeletePublicationAPIView(DestroyAPIView):
    queryset = Publication.objects.all()
    serializer_class = PublicationListSerializer
    permission_classes = [IsAuthorOrIsAdmin, ]


class FilterPublicationAPIView(ListAPIView):
    permission_classes = [AllowAny, ]
    queryset = Publication.objects.all()
    serializer_class = PublicationListSerializer

    def get_queryset(self):
        title = self.request.GET.get('title')
        queryset = super().get_queryset()
        queryset = queryset.filter(title__contains=title)
        return queryset


"""комментарии"""


class ListCommentAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CreateCommentAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class UpdateCommentAPIView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class DeleteCommentAPIView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentViewSet(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthor()]


# Чат
@csrf_exempt
def message_list(request, sender=None, receiver=None):
    print(request.user)
    if request.method == 'GET':
        sender = request.GET.get('sender')
        receiver = request.GET.get('receiver')
        sender_id = User.objects.get(username=sender)
        receiver_id = User.objects.get(username=receiver)
        messages = Message.objects.filter(sender=sender_id, receiver=receiver_id)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        if request.content_type == 'application/json':
            data = JSONParser().parse(request)
            serializer = MessageSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        else:
            message = request.POST['message']
            sender = request.POST['sender']
            receiver = request.POST['receiver']
            sender_id = User.objects.get(username=sender)
            receiver_id = User.objects.get(username=receiver)
            new_message = Message(sender=sender_id, receiver=receiver_id, message=message)
            new_message.save()
            serializer = MessageSerializer(new_message)
            return JsonResponse(serializer.data, safe=False)


# лайки
class LikeListCreate(APIView):

    def get(self, request, pk):  # метод для получения общего кол-ва лайков к определённому посту
        post = Publication.objects.filter(pk=pk)
        like_count = post.likepost.count()
        serializer = PublicationLikeSerializer(like_count, many=True)
        return Comment(serializer.data)

    def post(self, request, pk):  # метод для добавления лайков к посту
        like_users = request.user
        like_post = Publication.objects.filter(pk=pk)
        serializer = PublicationLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(like_users, like_post)
            return Comment(serializer.data, status=status.HTTP_201_CREATED)
        return Comment(serializer.errors, status=status.HTTP_400_BAD_REQUEST)