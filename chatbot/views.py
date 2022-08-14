from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def chatPage(request):
    return render(request, 'chatbot/main.html')


#@login_required(login_url='/users/login')
def room(request, room_name):
    return render(request, 'chatbot/index.html', {
        'room_name': room_name
    })
