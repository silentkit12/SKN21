import magic
import base64
from langchain_core.messages import HumanMessage, AIMessage

def get_file_mimetype(bytes_data: bytes):
    """파일을 bytes 타입으로 받아서 그 파일의 mime-type을 반환한다."""

    return magic.from_buffer(bytes_data, mime=True)


def get_human_message(text_message: str, bytes_data:bytes=None, mime_type=None, filename=None, history=None):
    """사용자 메시지와 선택적(Optional) 파일 첨부를 포함한 LangChain 메시지 리스트를 생성한다.
    대화 히스토리와 현재 사용자의 텍스트 메시지, 그리고 선택적으로 이미지나 PDF 등의 파일을 Base64로 인코딩하여 멀티모달 메시지 형태로 변환한다.

    Args:
        text_message (str): 사용자가 입력한 텍스트 메시지.
        bytes_data (bytes, optional): 첨부 파일의 바이트 데이터. Defaults to None.
        mime_type (str, optional): 첨부 파일의 MIME 타입 (예: 'image/png', 'application/pdf'). 
            Defaults to None.
        filename (str, optional): 첨부 파일의 이름. OpenAI PDF 전송 시 필요. 
            Defaults to None.
        history (list, optional): 이전 대화 히스토리. 각 항목은 'role'과 'message' 키를 
            포함하는 딕셔너리. Defaults to None.
        list: HumanMessage와 AIMessage 객체로 구성된 LangChain 메시지 리스트.
            마지막 항목은 현재 사용자 입력과 첨부 파일(있는 경우)을 포함한 HumanMessage.
    """

    # PDF 전송시 OpenAI는 파일이름을 전송해야한다.
    # https://python.langchain.com/docs/integrations/chat/openai/#multimodal-inputs-images-pdfs-audio

    # 입력 메세지들을 저장할 리스트
    messages = []

    # 이전 대화 히스토리 추가
    for message in history:
        if message['role'] == "user":
            messages.append(HumanMessage(content=message['message']))
        elif message['role'] == "ai":
            messages.append(AIMessage(content=message['message']))

    from pprint import pprint
    print("get_human_message history added:", messages)
    # 현재 사용자 입력 추가
    content=[
        {"type": "text", "text": text_message},
    ]
    if bytes_data: # 파일을 입력받았으면 멀티모달 추가
        d_type = "image" if "image" in mime_type else "file" # 이미지이면 "image" 아니면 file
        base64_data = base64.b64encode(bytes_data).decode("utf-8")
        content.append(
            {"type": d_type, "source_type":"base64", "data": base64_data, "mime_type": mime_type, "filename": filename}
        )
    messages.append(HumanMessage(content=content))
    return messages
   