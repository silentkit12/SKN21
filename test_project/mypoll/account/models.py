from django.db import models
from django.contrib.auth.models import AbstractUser
# 기존 Django에서 제공하는 User 모델을 확장해서 정의 - AbstractUser 상속해서 구현

# AbstractUser -> username, password
# CustomUser: 추가할 field들 정의 (name, email, birthday, [profile_image])
class CustomUser(AbstractUser):
    name = models.CharField(
        max_length=100,
        verbose_name="이름", #Form 관련 설정. ModelForm을 만들경우 form field 설정을 Model field에 한다.

    )
    email = models.EmailField( # DB-varchar, python-str: Email 유효성 검사를 한다.
        max_length=100,
        verbose_name="Email"
    )
    birthday = models.DateField( # DB: date 타입, python: datetime.date
        verbose_name="생일",
        null=True, #Nullable 컬럼
        blank=True, #Form 관련 설정. 빈 문자열(값)을 받을 수 있다.
    )

    def __str__(self):
        return f"username: {self.username}, name:{self.name}"
    