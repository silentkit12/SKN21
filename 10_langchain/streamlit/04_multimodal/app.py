import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import utils
import os

###################################################################################
# - chat_input에서 파일 첨부 받기
#   - accept_file(bool | str): True - 첨부가능, "multiple": 여러 파일 첨부가능
#    >> prompt = st.chat_input(placeholder="User:", accept_file=True)  
#
# - st.chat_input의 반환타입인 ChatInputValue의 attributes:
#   - ChatInputValue.text : 텍스트 입력
#   - ChatInputValue.files : 첨부파일을 List에 담아서 반환.
#     - 첨부파일은 UploadFile 타입
#
# - UploadFile attributes:
#     - name(str):  파일 명
#     - getvalue(): bytes - 첨부파일을 bytes로 반환.
###################################################################################

st.title("멀티모달 입력")

@st.cache_resource
def get_model():
    load_dotenv()
    model = ChatOpenAI(model="gpt-5-mini", streaming=True)
    return model

model = get_model()

######################################################
# session_state에 message_list(대화 히스토리) 를 추가.
######################################################s
if "message_list" not in st.session_state:
    st.session_state["message_list"] = []

###################################
# 기존 대화내용을 출력
###################################
for message in st.session_state['message_list']:
    with st.chat_message(message['role']):
        st.write(message["message"])

prompt = st.chat_input(
    placeholder="User:", 
    accept_file=True, 
    # file_type=["txt", "md", "pdf", "html", "jpeg", "jpg", "png"]  # 확장자로 첨부 파일 형식 제한.
)

###########################################
# 사용자가 입력한 텍스트와 첨부파일 처리
###########################################
if prompt:
    text_prompt = prompt.text # 텍스트 입력
    attach_files = prompt.files #첨부파일 : list
    mime_type=None
    bytes_data = None
    filename = None

    if attach_files:
        attach_file = attach_files[0]
        bytes_data = attach_file.getvalue() #bytes
        mime_type = utils.get_file_mimetype(bytes_data)
        filename = attach_file.name
        
    messages = utils.get_human_message(text_prompt, bytes_data, mime_type, filename, st.session_state['message_list'])

    st.session_state["message_list"].append({"role":"user", "message":text_prompt})
    
    with st.chat_message("user"):
        st.write(text_prompt)

    with st.chat_message("ai"):
        generator = model.stream(messages)
        full_message = st.write_stream(generator)
        st.session_state['message_list'].append({"role":"ai", "message":full_message})