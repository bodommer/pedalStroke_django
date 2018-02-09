from django.views import generic
from django.shortcuts import render

class BlogGeneralView(generic.View):

    def listAll(request):
        return render(request, 'blog/all_blogs.html')