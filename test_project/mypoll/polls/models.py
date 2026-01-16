# 모델 클래스들을 정의
from django.db import models

# 모델 클래스 정의 - Question(설문 질문) - Choice(설문의 보기)
##1.Models.Model 을 상속
##2. class 변수로 Field들을 정의 : Field == DB column, Model 객체의 Instance 변수. 이 둘에 대한 설정

# Create your models here.

#Modle class 정의 할 때 primary key Field를 선언하지 않으면.id (int outo_increment)으로 자동 생성
class Question(models.Model):
    #Field 정의 : 변수명 -(instance변수명, column 이름)
    #            Field 객체를 할당 Field 객체 - coulum 설정(type, null 허용여부,...)
    question_text = models.CharField(max_length=200) #CharField() -> 문자열타입(varchar)
    pub_date = models.DateTimeField(auto_now_add=True)
    #  DATETIMEField : 일시 타입(datetime, datetime.datetime)
    # auto_now_add: insert 될 때 일시를 자동 입력

    def __str__(self):
        return f"{self.id}. {self.question_text}"

#보기 테이블
class Choice(models.Model):

    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0) # 정수타입, (int, int)
    question = models.ForeignKey(
        Question, # 참조할 Model Class
        on_delete=models.CASCADE# 참조 값이 삭제된 경우 어떻게 하는지 -> chachde 삭제
    )  #FK -> Quesiont의 id를 참조.
    
    def __str__(self):
        return f"{self.id}. {self.choice_text}"
