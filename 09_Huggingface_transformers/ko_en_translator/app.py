# ko_en_translator/app.py
## Huggint face transformers.pipeline을 이용해서 한국어를 영어로 번역하는 앱

import streamlit as st
from transformers import pipeline

# 처음 시작할 때 한 번 실행하고 반환되는 리소스를 메모리에 저장하고, 다음부터는 그것을 사용.
@st.cache_resource
def get_model():
    model= "Helsinki-NLP/opus-mt-ko-en"
    pipe = pipeline(task="translation", model=model)
    return pipe

translator = get_model()

## 번역 내역을 저장할 session_state를 생성
# 어떤 값들을 계속 유지해야 할 때 저장하는 공간(dict 타입): session_state
if "history" not in st.session_state:
    st.session_state.history = [] # [(한국어 1, 번역 1), (한국어 2, 번역), ...] #st.session_state["history"]로도 가증.

st.title("한국어 - 영어 번역기")
st.subheader("한국어 문장을 입력하면 영어로 번역해 드립니다.")

st.text_input("번역할 한국어 문장을 입력하세요")
st.button("번역")