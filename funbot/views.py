from django.views import generic
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import random
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
from .models import UserChat
from django.db.models import F
from django.views.generic import TemplateView

def get_message_from_request(request):

    received_message = {}
    decoded_request = json.loads(request.body.decode('utf-8'))

    if 'message' in decoded_request:
        received_message = decoded_request['message'] 
        received_message['chat_id'] = received_message['from']['id'] # simply for easier reference

    return received_message

def save_model_data(chat_id,first_name,last_name,button):
    rst_userchat = UserChat.objects.get_or_create(chat_id = chat_id,first_name = first_name,last_name = last_name,button = button)
    rst_userchat[0].numberofcalls = F('numberofcalls') +1
    rst_userchat[0].save()      

def send_messages(message, token):
    # Ideally process message in some way. For now, let's just respond
    result_message = {}
    if message['text'] == '/start':
        post_message_url = "https://api.telegram.org/bot{0}/sendMessage".format(token)
        result_message['chat_id'] = message['chat_id']
        result_message['reply_markup'] = {"keyboard":[["Fat"],["Stupid"],['Dumb']]}
        result_message['resize_keyboard'] = True
        result_message['text'] = "Select a choice"
        response_msg = json.dumps(result_message)
        status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
        return
    jokes = {
         'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                    """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
         'fat':    ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                    """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
         'dumb':   ["""THis is fun""",
                    """THis isn't fun"""] 
    }

    post_message_url = "https://api.telegram.org/bot{0}/sendMessage".format(token)
    result_message['chat_id'] = message['chat_id']
    message_text = message['text'].lower()
    if 'fat' in message_text:
        result_message['text'] = random.choice(jokes['fat'])
        save_model_data(message.get('chat_id'),message['chat'].get('first_name'),message['chat'].get('last_name'),message_text)
    elif 'stupid' in message_text:
        result_message['text'] = random.choice(jokes['stupid'])
        save_model_data(message.get('chat_id'),message['chat'].get('first_name'),message['chat'].get('last_name'),message_text)

    elif 'dumb' in message_text:
        result_message['text'] = random.choice(jokes['dumb'])
        save_model_data(message.get('chat_id'),message['chat'].get('first_name'),message['chat'].get('last_name'),message_text)

    else:
        result_message['text'] = "I don't know any responses for that. If you're interested in yo mama jokes tell me fat, stupid or dumb."
    response_msg = json.dumps(result_message)
    status = requests.post(post_message_url, headers={
        "Content-Type": "application/json"}, data=response_msg)


class TelegramBotView(generic.View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)


    def get(self, request, *args, **kwargs):  
        return HttpResponse('Chat api works')

    def post(self, request, *args, **kwargs):
        TELEGRAM_TOKEN = '580277226:AAHXOMosSXyEX-zR-gMw0BXWqjLhA9Tn_cc'
        message = get_message_from_request(request)
        send_messages(message, TELEGRAM_TOKEN)

        return HttpResponse()

class ChatLogView(TemplateView):
    template_name = "chat_log.html"

    def get_context_data(self, **kwargs):
        context = super(ChatLogView, self).get_context_data(**kwargs)
        context['chat_logs'] = list(UserChat.objects.values('chat_id','button','numberofcalls'))
        context['chat_users'] = list(UserChat.objects.values('chat_id','first_name','last_name').distinct())
        # context['chat_users'].append({'chat_id':1515,'first_name':"asd",'last_name':"asd"})
        return context