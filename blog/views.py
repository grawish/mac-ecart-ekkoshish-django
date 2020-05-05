from django.shortcuts import render
from .models import Blog
from django.http import HttpResponse


# Create your views here.


def index(request):
    bloglist = []
    blog = Blog.objects.all()
    for each in blog:
        bloglist.append(each)
    return render(request, "blog/index.html", {"blog": bloglist})


def blogpost(request, bid):
    blog = Blog.objects.filter(id=bid)[0]

    return render(request, "blog/blogpost.html", {'blog': blog})
