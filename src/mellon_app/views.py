import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services.telegram import TelegramService


@csrf_exempt
def webhook(request):
    service = TelegramService()
    json_list = json.loads(request.body)
    chat_id = json_list['message']['chat']['id']
    service.send_message(chat_id, str(json_list))
    return HttpResponse()


def test(request):
    return JsonResponse({'status': 'true', 'message': 'worked'})
