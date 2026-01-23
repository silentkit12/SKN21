
//eventsourse객체.addEventListener("이벤트타입", 함수)
// DOMContentLoaded: HTML 문서가 Load되면 (HTML 응답받아서 화면이 구성되는 시점) - DOM Tree가 완성되면 발생하는 이벤트

document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    
    // 이벤트 처리함수 : 파라미터로 이벤트 객체를 받을 수 있다.
    // function handler(event: 발생한 이벤트 객체)
    chatForm.addEventListener('submit', (e) => {
        e.preventDefault(); //발생한 Event의 기본처리(handler)를 중단.
        // submit: form에서 전송

        const message = messageInput.value.trim();
        if (!message) return;

        //chatbot 창에 전달한 메시지를 출력
        // 출력할 메세지, "class 이름"
        // class 이름: user/ai message dlrjtdp Ekfktj ekfms tmxkdlffh cnffur
        appendMessage(message, 'user-message');
        messageInput.value = '';
        //messageInput 활성(false)/비활성화(True)
        //비활성화 AI 응답이 오는 동안은 입력하지 못 하게 한다.
        toggleForm(true);

        //AI 응답을 담을 ElementNode(div)를 저장할 변수.
        let aiMessageElement = null;

        //EventSourse: JS에서 SSE 지원 API
        //객체 생성(요청url)
        const eventSource = new EventSource(`/chat/stream/?message=${encodeURIComponent(message)}`);
        
        //EventSource에 Event Handler를 등록
        //onmessgae: 서버에서 메세지가 도착(message 이벤트) 할 때마다 호출되는 handler
        // onerror: 서버와의 연결 에러가 발생하면 호출되는 handler
        eventSource.onmessage = (event) => {
            if (event.data === '[DONE]') {
                eventSource.close();
                toggleForm(false);
                return;
            }
            //LLM 응답토큰을 받으면 처리.
            if (!aiMessageElement) {
                //첫번째 토큰을 받으면 <div class = 'message ai-message'></div> 생성
                //두번째 토큰 부터는 받은 토큰 문자열을 element에 append
                aiMessageElement = appendMessage('', 'ai-message');
            }

            if (event.data.startsWith('[ERROR]')) {
                aiMessageElement.innerHTML += `<span style="color: red;">${event.data}</span>`;
                eventSource.close();
                toggleForm(false);
            } else {
                aiMessageElement.innerHTML += event.data;
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        };

        eventSource.onerror = (err) => {
            console.error('EventSource 실패:', err);
            if (aiMessageElement) {
                aiMessageElement.innerHTML += `<span style="color: red;">[Error] 연결 실패</span>`;
            } else {
                appendMessage('<span style="color: red;">[Error] 연결 실패</span>', 'ai-message');
            }
            eventSource.close();
            toggleForm(false);
        };
    });

    function appendMessage(content, className) {
        const messageElement = document.createElement('div'); //<div>
        messageElement.setAttribute("class", `message ${className}`); //<div class="message className">
        messageElement.innerHTML = content; //<div class="message className">content</div>
        chatBox.appendChild(messageElement);//chatbot 창에 마지막 자식 노드로 추가.
        chatBox.scrollTop = chatBox.scrollHeight; // 스크롤을 아래로 내린다.
        return messageElement;
    }

    function toggleForm(disabled) {
        //elementNod.disabled: 노드를 활성/ 비활성화 시키는 속성
        messageInput.disabled = disabled;
        sendButton.disabled = disabled;
        if (!disabled) {//활성화 되면 메세지 입력으로 옮긴다.
            messageInput.focus();
        }
    }
});
