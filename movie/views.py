from django.shortcuts import render,redirect
from movie.models import *
from datetime import datetime
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponse
from django.views.decorators.http import require_http_methods
# Create your views here.
def index(request):
    return render(request,'index.html')

def movielist(request):
    movies = Movies.objects.all()
    context={
        "movies":movies,
    }
    return render(request,'movies-list.html',context=context)

def moviedetails(request,mid):
    movie= Movies.objects.get(pk=mid)
    comments=Comment.objects.filter(movie=movie)
    context={
        "movie":movie,
        "comments":comments,
    }
    if request.method=="POST":
        comment_body = request.POST["comment"]
        comment=Comment.objects.create(
            movie=movie,
            user=request.user,
            body=comment_body,
            created_date=datetime.now(),
        )
        return redirect(moviedetails)
    return render(request,'movie-detail.html', context=context)