#url Conf (Url Dispatcher, Url Mapping)
#url 경로와 view를 연결. 어떤 url로 요청이 들어오면 어떤 view가 실행될지를 연결 및 설정

"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


# from polls.views import welcome


urlpatterns = [
    path('admin/', admin.site.urls),
    #polls/ 시작하는 url경로로 요청이 들어오면 polls앱/urls.py 의 설정에 가서 나머지를 확인
    path("polls/", include("polls.urls")),
    path("account/", include("account.urls"))
    # path('polls/welcome', welcome, name="poll_welcome"), #1. client 요청경로 , 2. 호출할 view, 3. name="설정이름"
   
]

from django.conf.urls.static import static
from . import settings

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#MEDIA_URL 경로로 요청이 들어오면 어느 디렉토리를 찾아야 하는지 설정
## 개발 서버에서 설정 필요.
## 운영 환경(웹서버+MSGI)에서는 업로드 파일도 static 파일로 간주해서 웹 서버가 처리하도록 설정