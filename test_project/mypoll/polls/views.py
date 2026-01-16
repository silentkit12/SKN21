from django.shortcuts import render, redirect
from django.urls import reverse #url conf 의 설정 이름으로 url을 조회하는 함수
from datetime import datetime
from django.http import HttpResponse
from .models import Question, Choice

# Create your views here.

# 설문 welcome page
# 요청 -> 인삿말 화면 응답.

def welcome(request):
    print("welcome 실행")
    #요청처리
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #응답화면 생성 -> template 호출(template이 사용할 값을 전달. : now 값)
    response = render( #template을 호출 - 결과 -> HttpResponse 로 반환
        request, #HttpRequest
        "polls/welcome.html", #호출할 템플릿의 경로
        {"now":now} #template에 전달할 값들. name-value 로 전달
                    #Context Value 라고 한다.
    )
    print(type(response)) # server를 실행한 터미널에 출력
    return response


def welcome_old(request):
    print("welcome 실행")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #처리 결과 페이지 생성 -> html str 구현

    res_html = f"""<!doctype html>
<html>
    <head>
        <title>설문 main</title>
    </head> 
    <body>
        <h1>Welcom</h1>
        <p>저희 설문 페이지를 방문해주셔서 감사합니다.</p>
        현재시간: {now}
    </body>
</html>
"""
    res = HttpResponse(res_html)
    return res

# 설문(질문) 목록 조회
## 전체 question들을 조회해서 목록 html을 반환
## 요청 url : polls/list
## view 함수 : list
## template:polls/list.html

def list(request):
    # 1. DB에서 질문목록 조회 - > 모델 사용
    question_list = Question.objects.all().order_by("-pub_date")
    # 2. 응답페이지를 생성(template 사용) -> 반환
    return render(request,"polls/list.html", {"question_list":question_list})

# 개별 설문을 할 수 있는 페이지(설문 폼)로 이동
## 질문 id를 path parameter로 받아서 그 질문과 보기를 조회해서 화면에 출력
## 설문 입력 폼 작성
## path parameter : http://ip:port/path1/path2/path3/전달값1/전달값2
## request(요청)parameter: http://ip:port/path1/path2/path?name=전달값1&전달값2

# 요청 url:  /polls/vote_form/질문ID
# view 함수: vote_form
#template :  정상 polls/vote_form.html
##           오류 polls/error.html

def vote_form(request, question_id):
    #question_id 파라미터 -  path parameter 값을 받을 변수
    #view 함수의 두번째 파라미터 부터는 path parameter를 받을 변수들.
    ## 파라미터 변수명은 url.py에 등록한 변수명으로 선언하면 된다.

    #1. DB에서 question_id로 질문을 조회
    try:
        question = Question.objects.get(pk=question_id)
        # 응답화면 요청
        return render(
                request,
                "polls/vote_form.html",
                {"question":question}
            )
    except:
        return render(
            request,
            "polls/error.html",
            {"error_message": f"요청하신 {question_id}번 질문이 없습니다."}
        )



# 설문 처리 하기
## 선택한 보기(Choice)의 votes를 1 증가. 투표 결과를 보여주는 페이지로 이동

# 요청 URL :  polls/vote
# view 함수: vote
# 응답 :  정상- polls/vote_result.html
#         오류- polls/vote_form.html

#form 입력 -> 요청 파라미터로 읽는다.
#요청 파라미터: GET - request.GET -> dictionary {"요청 파라미터이름":"요청 파라미터 값"}
#              POST - request.POST -> dictionary

def vote(request):
    #요청 파라미터 조회
    choice_id = request.POST.get('choice') # 선택된 보기의 ID
    question_id = request.POST.get('question_id') # 질문 ID

    # choice-id가 넘어왔다면 choice 의 votes 를 증가
    if choice_id != None:
        selected_choice = Choice.objects.get(pk=choice_id)
        selected_choice.votes += 1
        selected_choice.save() # update

        #TODO: 업데이트 결과를 보여주는 View(vote_result)를 redirect 방식으로 요청
        #urls.py 에 path 에 등록된 이름으로 url을 등록
        # app_name:설정이름
        # path parameter 가 있는 경우 args=[path para 값, ..]

        # url = reverse("polls:vote_result", args=[question_id])
        # print(type(url), url)
        # return redirect(url)
    
        # 결과 페이지 - question을 조회
        question = Question.objects.get(pk=question_id)
        return render(
            request, "polls/vote_result.html", {"question":question}
        )
    else: # choice를 선택하지 않고 요청한 경우
        question = Question.objects.get(pk=question_id)
        return render(
            request,
            "polls/vote_form.html",
            {"question":question, "error_message":"보기를 선택하세요"}
        )

# 개별 질문의 투표 결과를 보여주는 View
# 요청 URL: /polls/vote_result/<question_id>
# View 함수: vote_result
# 응답 : polls/vote_result.html
def vote_result(request, question_id):
    question = Question.objects.get(pk=question_id)
    return render(
        request, "polls/vote_result.html", {"question":question}
    )