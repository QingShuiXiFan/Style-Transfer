from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.urls import reverse
import os
from django.contrib.auth import authenticate, login, logout  # 两个默认的用户认证和管理应用中的方法
from django.contrib import auth
from django.template import RequestContext
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User
import hashlib  # python的哈希加密库
from django.contrib.auth.hashers import make_password, check_password  # Django自带的哈希加密库
from django.core.mail import send_mail
import imghdr  # 判断是否是图片类型
import time, datetime
from django.conf import settings
from .models import Pictures

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = "common_static"
GPU_ISACTIVATED = True


# Create your views here.
def index(request):
    return render(request, "main/index.html")


def blog(request):
    return render(request, 'main/blog.html')


def blogArticle(request):
    return render(request, 'main/blogArticle.html')


def faq(request):
    return render(request, 'main/faq.html')


def about(request):
    return render(request, 'main/about.html')


def support(request):
    return render(request, 'main/support.html')


# 获得访问者的ip
def get_request_ip(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
        else:
            ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
    except:
        ip = None

    return ip


# 获取文件大小
def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize / float(1024 * 1024)
    return round(fsize, 2)


def ajaxUpload(request):
    if request.method == 'GET':
        return render(request, 'main/ajaxUpload.html')

    if request.method == 'POST':
        # 获取访问用户的ip
        ip = get_request_ip(request)

        # =======上传内容图片==========
        file_obj = request.FILES.get('file_obj', None)  # 获得文件对象，如果没有文件，则默认为None

        # 若没有上传图片
        if not file_obj:
            result = {"status": "no_file"}
            return JsonResponse(result)

        # 利用模型类　将图片要存放的路径存到数据库中
        t = time.time()  # 为文件名增加时间戳，用于独立标记每个文件
        timeStamp = str(int(t))
        p = Pictures()
        p.pic = "tmpImages/" + timeStamp + '_' + file_obj.name  # 文件路径字段
        p.uploaded_timeStamp = timeStamp  # 上传时间戳字段
        p.ip = ip  # 用户ip字段
        p.save()

        # 写入文件
        picPath = settings.MEDIA_ROOT + "/tmpImages/" + timeStamp + '_' + file_obj.name
        destination = open(picPath, 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in file_obj.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        # 把地址和id写入session
        request.session['uploaded_pic_path'] = str(p.pic)
        request.session['uploaded_pic_id'] = str(p.id)
        request.session.set_expiry(0)  # 关闭浏览器就清掉session

        picName = timeStamp + '_' + file_obj.name
        data = {"status": "success", "picName": picName}  # 返回data给前端，显示上传的图片
        return JsonResponse(data)


# 风格化
def transfer(request):
    if request.method == "GET":
        request.session.flush()  # 清除掉原有的session
        return render(request, 'main/transfer.html')

    if request.method == "POST":  # 请求方法为POST时，进行处理
        # 获取访问用户的ip
        ip = get_request_ip(request)

        style_name = str(request.POST.get('style_name'))  # 获取select的value值，如scream，与文件名对应，如scream.ckpt
        if style_name in ['la_muse','rain_princess','the_scream','the_shipwreck_of_the_minotaur','udnie','wave']:
            ckpt_path = style_name + ".ckpt"  # ckpt文件名
        else:
            ckpt_path = style_name
        content_name = str(request.POST.get('picName'))  # 获取内容图片名

        generated_image_path = BASE_DIR + "/" + STATIC_DIR + "/media/download/tmpImages/" + content_name  # 生成的图片路径
        # 若风格化后的图像已存在，则将之删除
        if (os.path.exists(generated_image_path)):
            os.remove(generated_image_path)

        # 执行evaluate.py程序
        cmd = settings.PYTHON_VERSION + " evaluate.py --checkpoint examples/checkpoint/" + ckpt_path + \
              " --in-path " + BASE_DIR + "/" + STATIC_DIR + "/media/upload/tmpImages/" + content_name + \
              " --out-path " + BASE_DIR + "/" + STATIC_DIR + "/media/download/tmpImages/"

        if (GPU_ISACTIVATED == True):
            activate_gpu = 'activate tensorflow-gpu'
            os.popen(activate_gpu + " && cd " + BASE_DIR + "/fast-style-transfer-master && " + cmd)
        else:
            os.popen("cd " + BASE_DIR + "/fast-style-transfer-master && " + cmd)

        start_time = time.time()
        while (os.path.exists(generated_image_path) == False):
            time_used = time.time() - start_time
            if time_used >= 60:
                data = {"status": "time_out"}
                return JsonResponse(data)
            else:
                time.sleep(1)

        data = {"status": "success"}  # 返回data给前端，显示上传的图片
        return JsonResponse(data)

# 下载图片
def file_down(request):
    file = open('', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="example.tar.gz"'
    return response


def showImg(request):
    return render(request, 'main/showImage.html')


def style2paint(request):
    return render(request, 'main/style2paint.html')


def user_login(request):
    if request.method == "GET":
        login_form = LoginForm()
        return render(request, 'main/login.html', {"form": login_form})
    if request.method == "POST":  # GET多用于数据查询，POST多用于数据写入或者更新等
        login_form = LoginForm(request.POST)  # request.POST是提交的表单数据所返回的类字典数据
        if login_form.is_valid():
            cd = login_form.cleaned_data
            # user = authenticate(email=cd['email'],
            #                     password=cd['password'])  # 若authenticate()内键值对上号了，则返回一个实例对象，否则返回None
            input_email = cd['email']
            input_password = cd['password']
            try:
                user = User.objects.get(email=input_email)
                if check_password(input_password, user.password):  # 哈希加密
                    login(request, user)  # 以上面返回的User实例对象作为参数，实现用户登录
                    return redirect('main:index')
                else:
                    message = "抱歉，您的密码填写错误"
                    return render(request, 'main/login.html', {"message": message, "form": login_form})
            except:
                message = "用户不存在！"
                return render(request, 'main/login.html', {"message": message, "form": login_form})
        else:
            message = "验证码输入错误"
            return render(request, 'main/login.html', {"message": message, "form": login_form})


def user_logout(request):
    logout(request)  # 注销用户
    return redirect("/main/")


def register(request):
    if request.user.is_authenticated:
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/main")
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():  # 获取数据
            # <== 这里可以加一些判断逻辑 ==>
            cd = user_form.cleaned_data
            input_username = cd['username']
            input_email = cd['email']
            input_password = cd['password']
            input_password2 = cd['password2']

            if input_password != input_password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'main/register.html', {"message": message, "form": user_form})
            else:
                same_name_user = User.objects.filter(username=input_username)
                if same_name_user:  # 用户名唯一
                    message = '该用户名已被注册，请使用别的用户名！'
                    return render(request, 'main/register.html', {"message": message, "form": user_form})

                same_email_user = User.objects.filter(email=input_email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'main/register.html', {"message": message, "form": user_form})

                # 若邮箱可以注册，且信息填写无误
                new_user = user_form.save(commit=False)
                new_user.password = make_password(user_form.cleaned_data['password'])  # 使用Django自带的哈希算法加密
                new_user.save()
                # send_mail('Subject here', 'Here is the message.', 'from@example.com',['to@example.com'], fail_silently=False)
                send_email_content = input_username + '，\n' + '\t你已经成功注册Style Transfer账号，以下是你的登录信息，请谨慎保存：\n' + '电子邮箱：' + input_email + '\n' + '密码：' + input_password + '\n\n' + 'www.styletransfer.cn'
                send_mail('[Style Transfer] Registered Successfully!', send_email_content, 'styletransfer@163.com',
                          [input_email],
                          fail_silently=False)
                message = input_username + "，注册成功！"

                return redirect('main:tip')
        else:
            message = "用户名已被使用"
            return render(request, "main/register.html", {"message": message, "form": user_form})
    user_form = RegistrationForm()
    return render(request, "main/register.html", {"form": user_form})


def playground(request):
    return render(request, 'main/playground.html')


def tip(request):
    return render(request, 'main/tip.html')


def hash_code(s, salt='styletransfer'):  # 哈希加密
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()
