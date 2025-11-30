from typing import Dict, Any
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_list(request) -> Response:
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )



@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def post_detail(request, pk: int) -> Response:
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if post.author != request.user:
            return Response(
                {'error': 'You are not the author of this post'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == 'DELETE':
        if post.author != request.user:
            return Response(
                {'error': 'You are not the author of this post'},
                status=status.HTTP_403_FORBIDDEN
            )
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, post_pk: int) -> Response:
    post = get_object_or_404(Post, pk=post_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(post=post, author=request.user)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_like(request, post_pk: int) -> Response:
    post = get_object_or_404(Post, pk=post_pk)
    like, created = Like.objects.get_or_create(post=post, user=request.user)

    if not created:
        like.delete()
        return Response(
            {'message': 'Like removed'},
            status=status.HTTP_200_OK
        )

    return Response(
        {'message': 'Like added'},
        status=status.HTTP_201_CREATED
    )



@api_view(['POST'])
def register_user(request) -> Response:
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')

    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email
    )

    return Response(
        {
            'message': 'User created successfully',
            'user_id': user.id,
            'username': user.username
        },
        status=status.HTTP_201_CREATED
    )