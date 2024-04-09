from django.shortcuts import render, redirect
from django.contrib import messages
from .models import tester_char_db
from .forms import LoginForm, UserCodeForm


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            tester_code = form.cleaned_data['user_code']
            password = form.cleaned_data['password']

            users = tester_char_db.objects.filter(tester_code=tester_code)
            if not users:
                messages.error(request, "該帳號不存在")

            else:
                user = users[0]
                if user.tester_password == password:
                    # 密码匹配，重定向到首页
                    request.session['tester_code'] = tester_code
                    return redirect('game_select')
                else:
                    # 密码不匹配
                    messages.error(request, "密碼錯誤")
    else:
        form = LoginForm()

    return render(request, 'games/login.html', {'form': form})


def create_account_view(request):
    if request.method == 'POST':
        form = UserCodeForm(request.POST)
        if form.is_valid():
            tester_code = form.cleaned_data['tester_code']

            # 检查数据库中是否已存在相同的 user_code
            if tester_char_db.objects.filter(tester_code=tester_code).exists():
                # 如果存在，显示警告信息
                messages.error(request, "該用戶名已被使用，請選擇其他用戶名")
            else:
                # 如果不存在，保存表单数据到数据库
                form.save()

                # 保存用户代码到 session 并重定向到登录页面
                request.session['tester_code'] = tester_code
                return redirect('game_login')

    else:
        form = UserCodeForm()

    return render(request, 'games/create_account.html', {'form': form})


def game_select_view(request):
    return render(request, 'games/game_select.html')
