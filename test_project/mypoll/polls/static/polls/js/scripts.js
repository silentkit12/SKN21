
function addChoice(){
        // "input[name$='choice_text']" input 태그 . name속성의 값이 choice_text로 끝나는 것.  name^='aa': aa로 시작, name='aa': aa 와 같은
        const choice_text_cnt = document.querySelectorAll("input[name$='choice_text']").length;
        const choice_input_name = `form-${choice_text_cnt}-choice_text`;

        const choice_input = document.createElement("input");
        choice_input.setAttribute("type", "text");
        choice_input.setAttribute("name", choice_input_name);
        choice_input.setAttribute("required", true);
        choice_input.setAttribute("class", "form-control");

        const layer = document.getElementById("choice_layer");
        layer.appendChild(choice_input);

        //formset으로 생성한 TOTAL_FORMS 값을 1 증가
        const totalForms = document.getElementById("id_form-TOTAL_FORMS");
        totalForms.value = parseInt(totalForms.value) + 1;
    }

    function delChoice(){
        const layer = document.querySelector("#choice_layer");
        if (layer.children.length > 2){
            layer.removeChild(layer.lastChild);         
        const totalForms = document.getElementById("id_form-TOTAL_FORMS")
        totalForms.value = parseInt(totalForms.value)-1;
        }
        else{
            //유지
            alert("보기가 두개이면 삭제가 안됩니다.");}
    }
