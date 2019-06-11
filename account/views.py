from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect


@csrf_protect
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('/accounts/')
        else:
            return render(request, 'account/login_index_page.html', {'message': '用户名或密码错误！', })
    # 返回一个无效帐户的错误
    else:
        return render(request, 'account/login_index_page.html', {'message': '用户名或密码错误！', })


def logout_view(request):
    logout(request)

    return redirect('/')


def form_view(request):

    return render(request, 'account/login_index_page.html')