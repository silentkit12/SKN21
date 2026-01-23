from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

# 사용자 정의 UserAdmin 정의
## 관리자 앱에서 User의 어떤 항목들을 관리할 지 정의
## UserAdmin을 상속해서 구현. admin.site.register()에 모델과 함께 등록

# UserAdmin에서 정의할 것 (class 변수로 정의)
# list_display: list -사용자 메인 화면에서 목록에 나올 항목들 정의
# add_fieldsets: tuple - 등룍 화면에 나올 항목들 지정
# fieldsets : tuple - 수정화면에 나올 항목들 지정

#field 개별항목
# list_display: list - 사용자 메인화면에서 몰곡에 나올 항목들 정의
# add_fieldset : tuple - 등록 화면에 ㅏㄴ올 항목들 지정
#fieldsets: tuple - 수정화면에 나올 항목들 지정

#field 개별항목
# fieldsets: field들을 그룹으로 묶은 것 (category)
class CustomUserAdmin(UserAdmin):
    #목록에 나올 User의 field 들
    list_display = ["username", "name", "email"]
    #등록화면 구성
    add_fieldsets = (
        ("인증정보",{"fields":("username", "password1", "password2" )}), #개별 fileds
        ("개인정보",{"fields":("name", "email", "birthday")}),
        ("권한",{"flelds":("is_staff", "is_superuser")})
    )
    #수정화면 구성
    add_fieldsets = (
        ("인증정보",{"fields":("username", "password")}), #개별 fileds
        ("개인정보",{"fields":("name", "email", "birthday")}),
        ("권한",{"flelds":("is_staff", "is_superuser")})
    )

admin.site.register(CustomUser, CustomUserAdmin)