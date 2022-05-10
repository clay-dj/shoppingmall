from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from django.http import HttpResponse,JsonResponse
from random import randint
from celery_tasks.sms.tasks import send_sms_code

#图片验证码
class ImageCodeView(View):
    def get(self,request,uuid):
        from libs.captcha.captcha import captcha

        text,image = captcha.generate_captcha()



        redis_conn = get_redis_connection('code')
        redis_conn.setex(uuid,300,text)

        return HttpResponse(image,content_type='image/jpeg')


#短信验证码
class SmsCodeView(View):
    def get(self,request,mobile):
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')

        if not all([image_code,uuid]):
            return JsonResponse({'code':400,'errmsg':'信息不全'})

        #连接redis数据库
        redis_cli = get_redis_connection('code')

        #获取redis数据
        redis_image_code = redis_cli.get(uuid)
        if redis_image_code is None:
            return JsonResponse({'code': 400, 'errmsg': '图片验证码已过期'})

        if redis_image_code.decode().lower()!= image_code.lower():
            return JsonResponse({'code':400,'errmsg':'图片验证码错误'})

        send_flag = redis_cli.get('send_flag_%s'%mobile)

        if send_flag is not None:
            return JsonResponse({'code': 400, 'errmsg': '不要频繁发送短信'})

        sms_code = '%06d'%randint(0,999999)

        pipeline = redis_cli.pipeline()

        pipeline.setex(mobile,300,sms_code)

        pipeline.setex('send_flag%s'%mobile,60,1)

        pipeline.execute()

        #
        # redis_cli.setex(mobile,300,sms_code)
        #
        # redis_cli.setex('send_flag%s'%mobile,60,1)

        #发送验证码
        # from libs.yuntongxun.sms import CCP
        # CCP().send_template_sms(mobile,[sms_code,5],1)


        send_sms_code.delay(mobile,sms_code)
        return JsonResponse({'code':0,'errmsg':'ok'})


#       celery_send_sms_code.delay()



# Create your views here.
