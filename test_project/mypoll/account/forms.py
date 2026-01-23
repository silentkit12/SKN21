
##Model form
## 기본 ModelForm : forms.ModelForm을 상속해서 정의
##                  Meta 내부 클래스에 어떤 모델의 어떤 필드를 이용해 정의할지 설정
##                  Model에 없는 것을 Form Field로 추가할 경우 class변수로 정의

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser # 지정한 Model의 Field들을 이용해 Form을 구성.

        # fields = "__all__" # 모델의 모든 Field들을 다 이용해서 Form을 구성
        # exclude = ["필드명"] #지정한 필드를 제외한 나머지를 이용해서 Form 구성
        fields = ["username", "password1", "password2", "name", "email", "birthday", "profile_img"]
        
        #Field의 기본 위젯(입력타입)을 변경할 때 Widget이 지정한다.
        #key: field - value: form widget 객체
        widgets = {
            "birthday":forms.DateInput(attrs={"type": "date"})
        }

        #검증 메소드 추가
    def clean_name(self):
        name = self.cleaned_data['name'] # 기본 검증 통과한 요청 파라미터 조회
        if len(name) < 2 : #이름은 두 글자 이상.
            raise forms.ValidationError("이름은 두 글자 이상 입력하세요")
        return name

class CutsomUserChangeForm(UserChangeForm):
    #패스워드 변경 메뉴는 나오지 않게 설정
    password = None

    class Meta:
        model = CustomUser
        fields = ["name", "email", "birthday","profile_img"]
        widgets = {
            "birthday":forms.DateInput(attrs={"type": "date"})
        }

    def clean_name(self):
        name = self.cleaned_data['name'] # 기본 검증 통과한 요청 파라미터 조회
        if len(name) < 2 : #이름은 두 글자 이상.
            raise forms.ValidationError("이름은 두 글자 이상 입력하세요")
        return name