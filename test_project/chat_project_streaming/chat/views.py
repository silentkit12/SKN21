from dotenv import load_dotenv

from django.shortcuts import render
from django.http import StreamingHttpResponse

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import trim_messages, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
import traceback

load_dotenv()


def get_chain():
    """LangChain 체인을 초기화"""

    prompt = ChatPromptTemplate(
        messages=[
            {
                "role": "system", 
                "content": ("당신은 다양한 분야에 대해 전문적인 조언을 할 수 있는 유능한 인공지능 Assistant입니다."
                            "사용자의 질문에 대해 친절한 톤으로 답변해 주세요."
                            "답변의 난이도가 질문에 명시되어 있지 않은 경우, 해당 주제를 처음 접하는 사람도 이해할 수 있도록 단계적으로 차근차근 쉽게 설명해 주세요."
                            "확실하지 않은 내용은 단정하지 말고 그 한계를 명확히 밝혀 주세요.")
            },
            MessagesPlaceholder(variable_name="history"),
            {"role": "user", "content": "{input}"}
        ]
    )
    chat = ChatOpenAI(model_name="gpt-5-mini")
    return prompt | chat
#챗봇 화면 응답
def index(request):
    return render(request, 'chat/index.html')

# 사용자 질의를 받아서 LLM에게 요청 -> 응답을 streaming으로 답
def stream_chat(request):
    #요청 파라미터 (GET 방식:디폴트)로 사용자 질의를 받는다. "message":"질의"
    message = request.GET.get('message', '')
    if not message:
        return StreamingHttpResponse("data: [ERROR] 메세지를 입력하세요.\n\n", content_type='text/event-stream')
    
    #session 에서 대화 히스토리(내역)을 저장. 없다면 만들어서(빈리스트)session에 저장
    if 'message_history' not in request.session:
        request.session['message_history'] = []
        request.session.modified = True # session 상태가 변경 되었음을 표시
        request.session.save() # 바뀐 상태를 저장/적용(보장)

#LLM 에 요청하고 streaming으로 응답을 받아서 제공하는 generatior
    def event_stream():
        try:
            message_history = request.session.get('message_history', [])

            chat = get_chain()
            ai_message = ""
            
            print(f"현재 히스토리: {len(message_history)}개 메시지")
            for chunk in chat.stream({"input": message, "history": message_history}):
                content = chunk.content.replace('\n', '<br>')
                if content:
                    ai_message += content
                    yield f"data: {content}\n\n"
            
            message_history.append(HumanMessage(content=message))
            message_history.append(AIMessage(content=ai_message.replace('<br>', '\n')))
            
            trimmed_msg = trim_messages(
                message_history,
                max_tokens=20, #최대 20개의 메시지만 유지
                strategy="last", #최근 것을 남기는 전략 <> 
                token_counter=len, # max_token 을 계산하는 방법 
                start_on="human", # 메세지 목록의 시작 ROLE
                end_on=("human", "ai"), # 메세지 목록의 마지막 ROLE
                include_system=True #system프롬프트 유지할지에 대한 여부
            )
            
            message_history_to_save = []
            #  session에 저장하기 위해서 휴먼메세지/AI메세지 타입의 객체를
            # 딕셔너리(OpenAI chat 형식)으로 변환해서 저장
            for msg in trimmed_msg:
                if isinstance(msg, HumanMessage):
                    message_history_to_save.append({"role": "user", "content": msg.content})
                elif isinstance(msg, AIMessage):
                    message_history_to_save.append({"role": "assistant", "content": msg.content})
            
            request.session['message_history'] = message_history_to_save
            request.session.modified = True
            request.session.save()
            
            print(f"저장된 히스토리: {len(message_history_to_save)}개 메시지")
            yield "data: [DONE]\n\n"

        except Exception as e:
            traceback.print_exc()
            yield f"data: [ERROR] {str(e)}\n\n"

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream') # iterable
    response['Cache-Control'] = 'no-cache'
   
    return response

