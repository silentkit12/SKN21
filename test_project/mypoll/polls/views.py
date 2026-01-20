from django.shortcuts import render, redirect
from django.urls import reverse #url conf 의 설정 이름으로 url을 조회하는 함수
from datetime import datetime
from django.http import HttpResponse
from .models import Question, Choice
from django.db import transaction #db transaction 처리
from django.core.paginator import Paginator

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
#################################
#페이징 처리 안 한 list
def list_old(request):
    # 1. DB에서 질문목록 조회 - > 모델 사용
    question_list = Question.objects.all().order_by("-pub_date")
    # 2. 응답페이지를 생성(template 사용) -> 반환
    return render(request,"polls/list.html", {"question_list":question_list})

####################
#페이징 처리 list
#
# - template 호출 전달할 Context Value
#   - 현재 페이지의 데이터 -page 객체
#   - 현재 페이지가 속한 그룹의 페이지 번호 start/end index
#   - 현재 페이지 그룹의 시작 페이지가 이전 페이지가 있는지 여부, 있다면 이전 페이지 번호
#   - 현재 페이지 그룹의 끝 페이지가 다음 페이지가 있는지 여부, 있다면 다음 페이지 번호

def list(request):
    paginate_by = 10 # 한 페이지당 데이터 개수
    page_group_count = 10 # 페이지 그룹당 페이지 수
    # http://ip:port/polls/list?page=6
    current_page = int(request.GET.get("page", 1)) #현재 조회요청이 들어온 페이지 번호. GET 방식의 요청파라미터

    #paginator
    q_list = Question.objects.all().order_by("-pk")
    pn = Paginator(q_list, paginate_by)

    #현재 페이지가 속한 Page
    start_index = int((current_page -1)/page_group_count)*page_group_count
    end_index = start_index + page_group_count

    page_range = pn.page_range[start_index : end_index] # 시작~끝페이지 번호조회

    #templet 에 전달할 context value dictionary
    context_value = {
        "page_range": page_range,
        "question_list": pn.page(current_page) #page[Question]
    }

    #pageGroup 의 시작페이지가 이전 페이지가 있는지 여부, 이전페이지 번호
    #PageGroup의 마지막 페이지가 다음페이지가 있는지 여부, 다음 페이지 번호

    start_page = pn.page(page_range[0]) # 시작 페이지 page 객체
    end_page = pn.page(page_range[-1]) # 마지막 페이지 page 객체

    if start_page.has_previous():
        context_value['has_previous'] = start_page.has_previous()
        context_value['previous_page_number']= start_page.previous_page_number()

    if end_page.has_next():
        context_value['has_next'] = end_page.has_next()
        context_value['next_page_number'] = end_page.next_page_number()

    # 응답 template 호출

    return render(
        request, "polls/list.html", context_value
    )



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
    except Exception as e :
        print(f"발생한 에러: {e}") # 터미널(서버창)에 실제 에러 이유를 출력
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

        url = reverse("polls:vote_result", args=[question_id])
        print(type(url), url)
        return redirect(url)
    
        # 결과 페이지 - question을 조회
        # question = Question.objects.get(pk=question_id)
        # return render(
        #     request, "polls/vote_result.html", {"question":question}
        # )
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


# 설문(질문)을 등록처리.
# 요청 URL: /polls/vote_create
# view 함수 : vote_create
#           - HTTP 요청 방식에 따라 입력 양식을 제공할지/ 처리할지 결정
#           - GET: 입력 양식 적용(설문문제와 보기를 입력할 수 있는 화면)
#           - POST: 등록처리
# 응답 :  - get c처리 : (template) polls/vote_create.html
#         - post 처리: redirect 방식 응답 ==> list_view 를 요청
# HTTP 요청방식 조회 - request.method(str:"GET", "POST")

def vote_create_old(request):
    http_method = request.method
    if http_method == "GET":
            #입력 처리
        return render(request, "polls/vote_create.html")

    elif http_method == "POST":
            # 등록처리
            # 1. 요청(path) 파라미터 읽기
            # 2. 요청 파라미터 검증. - 성공 -> 처리 , 실패 -> 입력폼페이지(에러페이지) 를 응답
            # 3. 업무처리 -> db작업
            # 4. 응답.

            # 요청파라미터 조회 - request.POST(GET) => dictionary 구현체
            # 요청 파라미터 중 question_text를 조회
        question_text = request.POST.get("question_text")
            # 요청파라미터 중 choice_text 를 조회(같은 이름으로 여러개 전달)
            # choice_text=보기1&choice_text=보기2&...
        choice_list = request.POST.getlist("choice_text") #list[str]

            # 요청파라미터 검증 (질문 : 1글자 이상, 보기: 2개 이상 각각 1글자 이상)
        if not question_text: #빈문자열일 경우
                return render(
                    request, "polls/vote_create.html",
                    {"error_msg": "문제를 한 글자 이상 입력하세요.",
                    "question_text":question_text,
                    "choice_list":choice_list}

                )    
            ## 보기 검증, choice_text가 넘어온 게 없거나
            ##          (choice_text가 넘어온 게 있는데 빈 문자열로 구성)
        if not choice_list or (choice_list and len([c for c in choice_list if c.strip()]) < 2):
                return render(
                    request, "polls/vote_create.html",
                    {"error_msg": "보기는 두개 이상 입력해야 합니다.",
                    "question_text":question_text,
                    "choice_list":choice_list}
                    )

        try:
            #with block을 정상적으로 처리하면 commit 발생
            #with block 실행중 Exception 이 발생하면 rollback(insert 처음 상태로 돌린다.)
            with transaction.atomic():

                #검증통과 -> DB에 저장(Instert)
                # 모델.save()
                q = Question(question_text=question_text) #id/pub_date 자동입력
                q.save()

                # raise Exception("문제가 발생했습니다.")

                for c in choice_list:
                    choice = Choice(choice_text=c, question=q) #id/vote 자동입력
                    choice.save()

        except Exception as e :
            # error page 이동
            return render(request, "error.html", {"error_message":"질문을 저장하는 도중 문제가 발생했습니다. 관리자에게 문의하세요"})

            # 4. 응답 - list로 redirect 방식으로 이동
        return redirect(reverse("polls:list"))
    
from .forms import QuestionForm, ChoiceFormSet

# forms.py 의 Form을 이용한 요청 파라미터 처리 view gkatn
def vote_create(request):
    
    if request.method == "GET":
        # 등록 폼 페이지 반환
        ## 등록 폼 -> forms.QuestionForm 을 이용
        q_form = QuestionForm() #질문
        c_formset = ChoiceFormSet() # 보기들
        #<input type=text> X extra 개수 => 이름(index로 관리)
        #   prefix-index 번호 - 필드 이름(form-0-choice_text, form-1-choice_text) < form이 디폴트 prefix. prefixsms 폼셋에 변수로 넣을 수 있음

        return render(
            request, "polls/vote_create_form.html", {"q_form":q_form, "c_formset": c_formset} 
        )

    elif request.method == "POST":
        #등록처리
        #요청파라미터 조회 + 검증 -> Form을 이용해서 조회 / 검증
        #요청 파라미터의 값을 속성으로 가지는 Form
        #요청 파라미터 조회해서 검증> 검증을 통과하면 Form객체에 넣는다.
        ## 요청파라미터 값들은 form의 dictionary 로 관리되고 cleaned_data 속성으로 조회가능
        q_form = QuestionForm(request.POST) 
        c_formset = ChoiceFormSet(request.POST) #prifix를 별도 정의했다면 여기서도 다시 지정해야함.
        # print("--------------------", q_form)
        # print("--------------------", c_formset)

        # 검증을 통과 했는지 여부 확인 - form.is_valid() : bool (True-통과, False- 검증 실패)
        if q_form.is_valid() and c_formset.is_valid():# 요청파라미터 검증에 문제 없으면
            #요청 파라미터 값들 조회. form 객체.cleaned_data: dict
            question_text = q_form.cleaned_data['question_text'] #key:필드이름
            choice_list = []
            for c_form in c_formset:
                choice_list.append(c_form.cleaned_data["choice_text"])

            #DB 저장
            try:
                with transaction.atomic():
                    q= Question(qeustion_text=question_text)
                    q.save()

                    for choice_text in choice_list:
                        c= Choice(choice_text=choice_text, question=q)
                        c.save()
            except:
                return render(request, "error.html", {"error_message":"질문/보기 DB 저장 중 문제발생"})
            
            return redirect(reverse("polls:list"))

        else: # 요청파라미터 검증 실패 => Form 객체는 ValidationError 객체를 가지고 있다.
            #에러 처리 페이지로 이동 -- > 등록페이지로 이동
            return render(
                request, "polls/vote_creat_form.html",
                {"q_form":q_form, "c_formset":c_formset} #검증 실패한 form 들을 전달
            )