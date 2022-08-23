from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.shortcuts import render, get_object_or_404

from .models import Movie, Review
from .serializers import MovieListSerializer, ReviewListSerializer

from django.contrib.auth import authenticate
import jwt
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

@api_view(['GET','POST'])
def movie_list_create(request):

    if request.method =='GET':
        movies = Movie.objects.all()
        serializer = MovieListSerializer(movies,many=True)

        return Response(data=serializer.data)
    
    if request.method =='POST':

        serializer= MovieListSerializer(data=request.data)
        #유효성 검사
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)


from django.shortcuts import render,get_object_or_404

@api_view(['GET','PATCH','DELETE'])
def movie_detail_update_delete(request,movie_pk):
    movie= get_object_or_404(Movie,pk=movie_pk)

    if request.method=='GET':
        serializer = MovieListSerializer(movie)
        return Response(serializer.data)

    if request.method == 'PATCH':
        serializer =MovieListSerializer(instance=movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    
    if request.method=='DELETE':
        movie.delete()
        data={
            'movie':movie_pk
        }
        return Response(data)

@api_view(['GET', 'POST'])
def review_list_create(request, movie_pk):

    if request.method == 'GET':
        reviews = Review.objects.filter(movie=movie_pk)
        serializer = ReviewListSerializer(reviews ,many=True)
        return Response(data=serializer.data)

    if request.method == 'POST':
        serializer = ReviewListSerializer(data=request.data)
        #유효성 검사
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)

@api_view(['GET', 'PATCH', 'DELETE'])
def review_detail_update_delete(request, review_pk, movie_pk):

    review = get_object_or_404(Review.objects.filter(movie=movie_pk),pk=review_pk)
    if request.method == 'GET':
        serializer = ReviewListSerializer(review)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = ReviewListSerializer(instance=review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        review.delete()
        data={
            'review': review_pk
        }
        return Response(data)

@api_view(["POST"])
@permission_classes([AllowAny])
def user_regist(request):
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return create_access_token(request.data)

# 로그인
@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    return create_access_token(request.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def test(request):
    return Response(request.user.username)

def create_access_token(data):
    username = data.get("username")
    password = data.get("password")
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        expired_at = (timezone.now() + timedelta(days=14)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        access_token = jwt.encode(
            {"user_id": user.id, "expired_at":expired_at},settings.SECRET_KEY)
        kwargs={}
        # kwargs["secure"] = True # https 배포를 하였을 때만!
        kwargs["httponly"] = True
        response = Response(access_token)
        response.set_cookie(
            "access_token", access_token, max_age=60 * 60 * 24 * 14, **kwargs
        )
        return response
    return Response( "Invalid username or password", status=status.HTTP_400_BAD_REQUEST)