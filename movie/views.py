from django.shortcuts import render,redirect
from movie.models import *
from datetime import datetime
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


# Create your views here.
def index(request):
    return render(request,'index.html')
@login_required
def movielist(request):
    movies = Movies.objects.all()
    context={
        "movies":movies,
    }
    if request.method=="POST" and request.user.is_superuser:
        mid=request.POST.get("mid")
        Movies.objects.get(pk=mid).delete()
        return HttpResponse(status=201)
    return render(request,'movies-list.html',context=context)
@login_required
def moviedetails(request,mid):
    movie= Movies.objects.get(pk=mid)
    comments=Comment.objects.filter(movie=movie)
    context={
        "movie":movie,
        "comments":comments,
    }
    if request.method=="POST":
        movie= Movies.objects.get(pk=mid)
        comments=Comment.objects.filter(movie=movie)
        allcomments=[]
        for comment in comments:
            allcomments.append({"body":comment.body,"name":comment.user.get_full_name(),"date":comment.created_date})
        
        #serialized_obj = serializers.serialize('json',allcomments)
        return JsonResponse(allcomments,safe=False)
    return render(request,'movie-detail.html', context=context)
@login_required
def addcomment(request):
    comment_body = request.POST.get("comment")
    mid=request.POST.get("mid")
    movie=Movies.objects.get(pk=mid)
    comment=Comment.objects.create(
        movie=movie,
        user=request.user,
        body=comment_body,
    )
    return HttpResponse(status=201)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def newmovie(request):
    if request.method=="POST":
        try:
            title=request.POST['title']
            director=request.POST['director']
            actors=request.POST['actors']
            release_date=request.POST['release_date']
            movie_url=request.POST['movie_url']
            description=request.POST['description']
        except:
            return render(request,'new-movie.html',{'msg':"Fill All The Fields"})
        movie = Movies.objects.create(
            title = title,
            release_date = release_date,
            actors=actors,
            movie_url = movie_url,
            description = description,
            director = director
        )
        movie.save()
        return redirect('movies-list')
    else:
        return render(request, 'new-movie.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def updatedata(request):
    title=request.POST.get('title')
    director=request.POST.get('director')
    actors=request.POST.get('actors')
    release_date=request.POST.get('release_date')
    movie_url=request.POST.get('movie_url')
    description=request.POST.get('description')
    mid=request.POST.get("mid")
    movie=Movies.objects.get(pk=mid)
    movie.title=title
    movie.director=director
    movie.actors=actors
    movie.movie_url=movie_url
    movie.description=description
    movie.save()
    return HttpResponse(status=201)