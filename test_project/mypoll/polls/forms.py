# polls/froms.py

from django import forms

# Form 클래스를 정의 - Forms.Form 을 상속
## Form 클래스 : 입력 폼들을 모아서 정의한 클래스
##     -Form Field: 개별 입력 폼(input) 들을 정의
##                  클래스 변수로 정의. 입력 폼 양식 - 파이썬 타입 관련되어 FormField 객체를 할당

## 설문 질문 등록 폼
class QuestionForm(forms.Form):
    #Form Field - > 질문 입력
    #변수명 (요청 파라미터 name) = FormField(): 어떤 값을 입력 받을지 타입.
    #Form Field 1개 -> 한개 이름의요청파라미터 입력 태그를 설정
    ## 같은 이름으로 여러개 입력을 받을 경우 -> Form set 이용해서 구현
    question_text = forms.CharField( # 문자열 입력 폼 - View 에서 문자열로 읽기
        label="", #입력에 대한 label을 설정.
        max_length=200, # 최대 입력 글자 수.
        required=True, # 필수 입력인지 여부
        widget=forms.TextInput( #widget은 input 태그를 지정.
            attrs={"class": "form-control"} #입력 tag의 attribute 설정
        )
    )
     #검증 메소드를 추가. -> 업무규칙에 의한 검증
        #메소드 이름 규칙 : 1. 개별 Field들을 검증 - clean_필드명
        #                  2. 전체 입력 데이터들을 검증 - clean
        # 검증 메소드는 기본 검증을 하고 나서 호출한다.
        # - 구현 : 검증 통과 - return 요청파라미터 값. 검증오류 : raise ValidationError
        
    def clean_question_text(self):
        txt = self.cleaned_data['question_text'].strip() # 기본 검증을 통과한 입력값
        if len(txt) <= 5:
            raise forms.ValidationError("질문은 6글자 이상 입력하세요")

        return txt


class ChoiceForm(forms.Form):

    choice_text = forms.CharField(
        label="", #라벨을 생성하지 않게 한다.
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={"class":"form-control"})
    )
    def clean_question_text(self):
        txt = self.cleaned_data['question_text'].strip() # 기본 검증을 통과한 입력값
        if len(txt) <= 2:
            raise forms.ValidationError("보기는 2글자 이상 입력하세요")

        return txt

#ChoiceForm을 이용해서 FormSet 클래스를 성장
# FormSet : Form + Set : Form들의 집합
#           Form클래스의 내용을 붕복해서 가지는 class
#           특정 input 양식을 반복적으로 여러개 가지는 입력 페이지를 구성할 때
#           같은 이름으로 여러개의 입력을 받아야 할 때

ChoiceFormSet = forms.formset_factory(
    ChoiceForm, #Form클래스
    extra=2 #Form 을 몇 개 반복해서 만들지 갯수
)