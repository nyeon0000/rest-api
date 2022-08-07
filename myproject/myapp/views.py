from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Movie
from .models import Review
from .serializers import MovieListSerializer

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

@api_view(['GET','POST'])
def review_create(request, id):
    if request.method == "POST":
        review= get_object_or_404(Movie,pk=review_pk)
        serializer = MovieListSerializer(movie)
        post = get_object_or_404(Post, pk=id)
        current_user = request.user
        comment_content = request.POST.get("content")
        if len(comment_content.strip()) != 0:
            Comment.objects.create(content=comment_content,
                                   writer=current_user, post=post)
    return Response(serializer.data)


def review_edit(request, id):
    comment = Comment.objects.get(id=id)
    if request.user == comment.writer:
        return render(request, "main/comment_edit.html", {"comment": comment})
    else:
        return Response("main:detail", comment.post.id)


def review_delete(request, id):
    comment = Comment.objects.get(id=id)
    if request.user == comment.writer:
        comment.delete()
    return Response("main:detail", comment.post.id)


def review_update(request, id):
    comment = Comment.objects.get(id=id)
    comment.content = request.POST.get("content")
    comment.save()
    return Response("main:detail", comment.post.id)