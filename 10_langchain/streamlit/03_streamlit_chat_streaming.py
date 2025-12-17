# 03_streamlit_chat_streaming

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import streamlit as st

@st.cache_resource
def get_model():
    #OpenAI GPT 모델 연동
    load_dotenv()
    return ChatOpenAI(model="gpt-5-mini")

@st.cache_resource
def get_prompt_template():
    prompt = ChatPromptTemplate(
        [
            {"role":"system", "content":"당신은 유능한 인공지능 Assistant입니다."},
            MessagesPlaceholder("history"),
            {"role":"user", "content":"{query}"}
        ]
    )
    return prompt

model = get_model()
prompt = get_prompt_template()

if "chat_history" not in st.session_state:
    st.session_state['chat_history'] = []

st.title("Chatbot Service")

################
#기존대화내역출력 
# - session_state 저장된 대화내역을 chat_message()를 이용해 출력
################
for chat_dict in st.session_state['chat_history']:
    with st.chat_message(chat_dict['role']):
        st.write(chat_dict['content'])


user_input = st.chat_input("User:")

if user_input: # 사용자가 질문을 입력하면
    #사용자 질문을 출력
    with st.chat_message("user"):
        st.write(user_input)
    # PromptTemplate 로 쿼리 생성
    query = prompt.invoke({
        "query":user_input,
        "history":st.session_state['chat_history']
    })    
    # llm에 요청 - stream()
    generator = model.stream(query)
    with st.chat_message("ai"):
        response = st.write_stream(generator) # generator가 값을 제공하는데로 출력하고 최종 출력한 내용을 반환.

    # 대화 내역을 session state에 저장
    st.session_state['chat_history'].append(
        {"role":"user", "content":user_input}
    )
    st.session_state['chat_history'].append(
        {"role":"ai","content":response}
    )



#uv run streamlit run 03_streamlit_chat_streaming.py 