# run.py

import my_module # my module / 현재 실행모듈이(run.py)와 같은 디랙토리(package)에서 불러오는 모듈을 찾는다.

r = my_module.plus(100, 200) # module.함수()

#import my_package.todo_module as todo # as 별칭 my_package.todo_module 대신 todo를 사용. #별칭 사용시 별칭만 사용해야 함.
#현재 실행모듈이(run.py)와 다른 디랙토리(package)에서 불러오는 모듈을 찾는다

from my_package import todo_module # as todo 

#print(r)
#r = my_module.minus(130, 100)
#print(r)

#my_package 모듈 안에 있는 todo_module 를 실행(사용)

#my_package.todo_module.print_gugudan(5) # 별칭을 사용해서 에러가 남
#todo.print_gugudan(3)
todo_module.print_gugudan(2)

# plus()
#python run.py