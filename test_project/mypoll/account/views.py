from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import (
    authenticate, # 인증확인 : username, password를 DB에서 확인
    login,  # 로그인 처리 -로그인한 사용자 정보(User Model)를 session에 추가
    logout, # 로그 아웃 처리 - session에서 사용자 정보를 제거
    update_session_auth_hash, # 회원정보 수정처리에서 사용. session의 사용자 정보를 수정한 것을 변경.
    get_user
    )
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required

from .models import CustomUser
from .forms import CutsomUserChangeForm, CustomUserCreationForm

#가입 처리
#요청 URL : account/create
#View 함수 : create
#           -GET: 가입 입력페이지를 반환
#           -POST: 가입처리
# 응답
#       -GET: templetes/account.create.html
#       -POST: main으로 이동.(root/home.html)

def create(request):

    if request.method == "GET":
        return render(
            request,
            "account/create.html",
            {"form":CustomUserCreationForm()}
        )
    elif request.method == "POST":
        # 가입처리
        #1. 요청 파라미터 조회 및 검증
        #request.POST: 일반 요청파라미터(text) 저장
        #request.FILES: 업로드 된 파일(요청 파라미터)
        form = CustomUserCreationForm(request.POST, request.FILES)
        #업로드 된 파일을 설정된 저장경로에 저장하고 그 경로를 Field에 가지고 있는다.

        if form.is_valid():
        #2. DB에 저장
        #ModelForm은 save()메소드를 제공. 요청파라미터 값들을 DB에 insert/update 해준다.
            user = form.save() # 반환: save() 처리한 Model 객체를 반환.
            print(type(user), user)


        #3. 응답
            return redirect(reverse("polls:welcome"))

        else: # 요청 파라미터에 문제가 있는 경우
            return render(
                request,
                "account/create.html",
                {"form":form} # 문제가 있는 Formdmf context value로 전달.
            )
# 가입한 사용자 정보 조회
# URL: /account/detail/<user_id> (TODO: user_id 는 나중에 로그인 처리후 변경)
# 함수 : detail
# 응답 : account/detail.html

@login_required
def detail(request):
    try:
        #로그인한 사용자의 user로 부터 id를 조회
        # get_user(request)/request.user : 로그인한 User모델 객체
        user_id = get_user(request).pk
        user = CustomUser.objects.get(pk=user_id)
        return render(
            request, "account/detail.html", {"user":user}
        )

    except:
        return render(request, "error.html", {"error_message": "회원정보 조회도중 문제가 발생헸습니다."})
    

#로그인처리
#요청 url: /account/login
#함수 user_login
#       -GET: 로그인 폼 페이지로 이동(account/login.html)
#       -POST: 로그인 처리 (redirect-> polls:welcome)

def user_login(request):
    if request.method == "GET":
        return render(
            request, "account/login.html", {"form":AuthenticationForm()}
        )
    elif request.method == "POST":
        #로그인 처리
        ##요청 파라미터(username, password) whghl
        username = request.POST['username']
        password = request.POST['password']
        ## DB로 부터 조회(username과 password가 일치하는지)
        ## 반환: User Model(일치), None(불일치)
        user = authenticate(request, username=username, password=password)
        if user is not None: 
            #일치 - 로그인 처리(session에 로그인 사용자 정보-UserModel-을 저장정)
            login(request, user) #session에 user를 등록

            if request.GET.get("next"): #next 쿼리 스트링이 있다면
                #로그인한 상태에서 호출해야하는 url을 하지 않고 호출한 경우 원래 요청한 url로 
                return redirect(request.GET.get("next"))

            return redirect(reverse("polls:welcome"))
        else: 
            ## 불일치 - 로그인 화면으로 이동
            return render(request, "account/login.html", {"form":AuthenticationForm(), "error_msg":"username, password를 다시 확인하세요."})
        
#로그아웃 처리
## /account/logout
##view 함수 : user_logout
##응답: redirect - polls:welcome

@login_required
def user_logout(request):
    #로그인시 호출햇던 login() 함수가 처리된 것을 무효화처리(session에서 user정보를 )
    logout(request)
    return redirect(reverse("polls:welcome"))


#로그인 한 회원정보 수정
#url : /account/update
#view: update
#       -GET: 수정폼 페이지를 반환(account/update.html)
#       -POST: 수정처리(redirect:account:detail view)

@login_required
def update(request):
    if request.method == "GET":
        #CustomUserChangeForm 이용
        ## 수정 폼 : 객체 생성 시 수정할 모델 객체를 전달
        form = CutsomUserChangeForm(instance=get_user(request))
        return render(request, "account/update.html", {"form":form})

    elif request.method == "POST":
        #수정 처리
        #1. 요청 파라미터 조회 +검승
        form = CutsomUserChangeForm(request.POST, request.FILES, instance=get_user(request))

        if form.is_valid():
            #DB에 저장
            user = form.save()
            #session의 저장된 User 정보를 수정된 것으로 변경.
            update_session_auth_hash(request, user)
            #상세페이지 요청
            return redirect(reverse("account:detail"))
        else:
            return render(request, "account/update.html", {"form":form})
        
#password 변경 처리
#요청 url : /account/password_change
#view 함수 : password_change
#처리 - GET : 패스워드 변경 폼 페이지 이동 (account/password_change.html)
#      POST : 패스워드 변경 처리 (redirect - account:detail)

@login_required
def password_change(request):
    
    if request.method == "GET":
        form = PasswordChangeForm(get_user(request))
        return render(request, "account/password_change.html", {'form':form})
    
    elif request.method == "POST":
        form = PasswordChangeForm(get_user(request), request.POST)
        if form.is_valid():
            #DB에 저장
            user = form.save()
            update_session_auth_hash(request,user)
            #응답
            return redirect(reverse("account:detail"))
        else:
            return render(request, "account/password_change.html", {"form":form})
        

# 사용자 삭제(탈퇴)처리
# 요청 url : /account/delet
# view 함수 : user_delete
# 응답 : redirect - polls:welcome

@login_required
def user_delete(request):
    #로그인 한 사용자를 삭제
    user = get_user(request) #로그인 한 사용자 Model
    user.delete() #DB에서 삭제
    #로그아웃
    logout(request)
    return redirect(reverse("polls:welcome"))

