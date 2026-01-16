from django.contrib import admin

from .models import Question, Choice
# .models -> .: 현재 모듈(admin.py)과 같은 패키지를 가리킨다.

# Register your models here.
# 관리자 앱에서 Model의  Data를 관리할 수 있도록 등록
## admin.site.register(모델클래스)

admin.site.register(Question)
admin.site.register(Choice)

# 모델 클래스 정의 한 후에 DAtabase에 적용
# Project Root > python manage.py makemigrations # 모든 app 들에 적용
#                python manage.py makemigrations polls # polls app 에만 적용
# ->table에 적용(생성, 수정)할 코드 를 작성.
# python manage.py migrate #DB에 적용 (table생성, 수정)
