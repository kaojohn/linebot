from django.shortcuts import render
from datetime import datetime
import json
import random
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, ImageSendMessage

from crawel.invoice import get_invoice_numbers, search_invoice_bingo

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parse = WebhookParser(settings.LINE_CHANNEL_SECRET)
start_invoice = False


@csrf_exempt
def callback(request):
    global start_invoice
    if request.method == "POST":
        signature = request.META["HTTP_X_LINE_SIGNATURE"]
        body = request.body.decode("utf-8")
        try:
            events = parse.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                message = event.message.text
                message_object = None
                if start_invoice:
                    if meaaage == "0":
                        start_invoice = False
                        message_text = "離開兌獎模式"
                    else:
                        message_text = "進入兌獎模式(0:out!)"

                    message_object = TextSendMessage(text=message_text)

                elif message == "1":
                    numbers = get_invoice_numbers()
                    message_text = "本次發票號碼為:" + "\n" + "\n".join(numbers)
                    message_text += "\n請開始輸入號碼"
                    message_object = TextSendMessage(text=message_text)
                    start_invoice = True

                elif message == "你來了":
                    message_object = TextSendMessage(text="我來了")
                elif "樂透" in message:
                    reply_message = "預測號碼為:\n" + get_lottory_number()
                    message_object = TextSendMessage(text=reply_message)
                elif "捷運" in message:
                    if "台中" in message:
                        image_url = "https://assets.piliapp.com/s3pxy/mrt_taiwan/taichung/20201112_zh.png?v=2"
                    if "高雄" in message:
                        image_url = "https://upload.wikimedia.org/wikipedia/commons/5/56/%E9%AB%98%E9%9B%84%E6%8D%B7%E9%81%8B%E8%B7%AF%E7%B6%B2%E5%9C%96_%282020%29.png"
                    else:
                        image_url = "https://assets.piliapp.com/s3pxy/mrt_taiwan/taipei/20230214_zh.png"
                    message_object = ImageSendMessage(
                        original_content_url=image_url, preview_image_url=image_url
                    )

                else:
                    message_object = TextSendMessage("0.0??")
                line_bot_api.reply_message(
                    event.reply_token,
                    message_object,
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


# Create your views here.
def get_books(request):
    mybook = {1: "hbo", 2: "reunbo", 3: "r-bo"}

    return HttpResponse(json.dumps(mybook))


def index(request):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return HttpResponse(f"<h1>現在時刻:{now}</h1>")


def get_lottory_number():
    numbers = sorted(random.sample(range(1, 49), 6))
    x = random.randint(1, 49)
    number_str = " ".join(map(str, numbers)) + f" 特別號:{x}"
    return number_str


def lottory(request):
    numbers = sorted(random.sample(range(1, 49), 6))
    x = random.randint(1, 49)
    number_str = " ".join(map(str, numbers))
    return render(request, "lottory.html", {"numbers": number_str, "x": x})


def lottory_2(request):
    numbers = sorted(random.sample(range(1, 49), 6))
    x = random.randint(1, 49)
    number_str = " ".join(map(str, numbers))
    return HttpResponse(f"<h1>號碼:{number_str}特別號:{x}</h1>")
