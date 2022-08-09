from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, get_object_or_404

from .models import Movie, Review
from .serializers import MovieListSerializer, ReviewListSerializer

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
def review_list_create(request):

    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewListSerializer(reviews ,many=True)
        return Response(data=serializer.data)

    if request.method == 'POST':
        serializer = ReviewListSerializer(data=request.data)
        #유효성 검사
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)

@api_view(['GET', 'PATCH', 'DELETE'])
def review_detail_update_delete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

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