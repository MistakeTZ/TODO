from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest


def index(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return render(request, 'main/index.html')
    else:
        return redirect('login')
