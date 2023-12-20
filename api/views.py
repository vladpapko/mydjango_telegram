from .models import BotUser, Feedback
from .serializers import BotUserSerializer, FeedbackSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import BotUser
import requests
from django.shortcuts import render


class BotUsersApiView(ListCreateAPIView):
    queryset = BotUser.objects.all() 
    serializer_class  = BotUserSerializer

class FeedbacksApiView(ListCreateAPIView):
    queryset = Feedback.objects.all() # запрос к базе данные и извлечение отзывов
    serializer_class  = FeedbackSerializer

class BotUserUpdateAPIView(RetrieveUpdateAPIView):
    queryset = BotUser.objects.all()
    serializer_class = BotUserSerializer #serializer - преобразуют данные сложных типо в python и обратно
    lookup_field = 'user_id'


def broadcast_message_view(request):
    return render(request, 'broadcast.html')


@csrf_exempt # данные, которые сервер отправляет браузеру в ожидании получить их обратно
def send_broadcast_message(request):
    if request.method == 'POST':                          # предназначен для направления запроса, при котором веб-сервер принимает данные, заключённые в тело сообщения, для хранения
        message = request.POST.get('message', '')  # получаем сообщение
        subscribers = BotUser.objects.filter(subscribed=True)
        bot_token = '6768312843:AAFbscy6xZSBLygMbDoCUR5D8_znDS6Fylw' 

        for subscriber in subscribers:
            url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
            data = {'chat_id': subscriber.user_id, 'text': message}
            requests.post(url, data=data)

        return HttpResponse('Сообщение отправлено.')
    else:
        return HttpResponse('Ошибка', status=400)