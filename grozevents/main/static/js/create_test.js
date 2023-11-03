let test_data ={
    'test_name': '',
    'questions': [
        {
            'question': '',
            'answers': [
                {
                    'answer': '',
                    'is_correct': false
                },
                {
                    'answer': '',
                    'is_correct': false
                }
            ]
        }
    ]
}

const question_html = `                    
<li class="question_parent_id">
    <div class="input-group">
        <label>Вопрос {{ index }}:</label>
        <input class="question_id" type="text" placeholder="Введите вопрос..." value="{{ value }}" required>
    </div>

    <ul>
        {{ answers }}
    </ul>
</li>
<br> <hr> <br>
`

const answer_html = `
<li>
    <div class="input-group">
        <label>Вариант ответа {{ index }}:</label>
        <div class="input-with-checkbox ">
            <input class="answer_id" type="text" placeholder="Введите варинт ответа..." value="{{ value }}" required>
            
            <label class="checkbox-other">
            <input class="answer_checkbox_id" type="checkbox" {{ checked }}>
            <span></span>
            </label>

        </div>
    </div>
</li>
`

const add_answer_button_html = `
    <div class="container">
        <button onclick="add_answers({{ index }})" class="add-button gradient-button"><a>+</a></button>
    </div>
`

function start(){
    refresh_html();
}

function refresh_html(){
    const test_name_element = document.getElementById('test_name');
    const questions_element = document.getElementById('questions');

    test_name_element.value = test_data.test_name;

    let questions_html = ''
    for (let i = 0; i < test_data.questions.length; i++){

        let question = test_data.questions[i];
        let answers_html = ''

        for (let ans_index = 0; ans_index < question.answers.length; ans_index++){

            let checked = '';
            if (question.answers[ans_index].is_correct) {
                checked = 'checked'
            }
            answers_html += answer_html
                .replace('{{ index }}', (ans_index + 1).toString())
                .replace('{{ value }}', question.answers[ans_index].answer)
                .replace('{{ checked }}', checked);
        }

        answers_html += add_answer_button_html.replace('{{ index }}', i.toString());

        questions_html += question_html
            .replace('{{ index }}', (i + 1).toString())
            .replace('{{ answers }}', answers_html)
            .replace('{{ value }}', question.question);
    }

    questions_element.innerHTML = questions_html;
}

function refresh_data(){
    const test_name_element = document.getElementById('test_name');
    const questions_element = document.getElementById('questions');
    const question_elements = document.querySelectorAll('.question_parent_id')

    test_data.test_name = test_name_element.value;

    for (let question_i = 0; question_i < question_elements.length; ++question_i){
        const question_element = question_elements[question_i];
        const answers_elements = question_element.getElementsByClassName('answer_id')
        const answers_checkbox_elements = question_element.getElementsByClassName('answer_checkbox_id')

        test_data.questions[question_i].question = question_element.querySelector('.question_id') .value;

        for (let answer_i = 0; answer_i < answers_elements.length; ++answer_i){
            const answer_element = answers_elements[answer_i];
            const answer_checkbox_element = answers_checkbox_elements[answer_i];

            test_data.questions[question_i].answers[answer_i].answer = answer_element.value;
            test_data.questions[question_i].answers[answer_i].is_correct = answer_checkbox_element.checked;
        }
    }
}

function add_question(){
    test_data.questions.push({
        'question': '',
        'answers': [
            {
                'answer': '',
                'is_correct': false
            },
            {
                'answer': '',
                'is_correct': false
            }
        ]
    })

    refresh_data();
    refresh_html();
}

function add_answers(question_index){
    test_data.questions[question_index].answers.push({
        'answer': '',
        'is_correct': false
    });
    refresh_data();
    refresh_html();
}


const form_element = document.getElementById("form");
console.log(form_element);

form_element.addEventListener("submit", function(event) {
    event.preventDefault(); // Предотвращаем стандартную отправку формы

    let formData = new FormData(form_element);
    const jsonData = JSON.stringify(test_data);
    formData.append("test_data", jsonData);

    const url = "/create_test/";
    let xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);

    xhr.onload = function() {
        if (xhr.status === 200) {
            console.log("Успешно отправлено:", xhr.responseText);
            window.location.replace("/create_test/");
        } else {
            console.log("Ошибка:", xhr.responseText);
        }
    };

    xhr.send(formData);
});

start();