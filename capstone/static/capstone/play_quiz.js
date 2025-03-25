document.addEventListener('DOMContentLoaded', () => {
    /* Define question index. From 0 to N-1. Where N is the number of questions in the quiz.*/
    var n = 0;
    /* Define N, the number of questions in the quiz */
    /* Get value of N from html page. First get value of N from count() in play_quiz route */
    var N = document.querySelector('#number_questions').dataset.number_questions;

    /* quiz_score declared here so global scope */
    var quiz_score = 0;

    /* Create score element */
    const score_pElem = document.createElement("p");

    /* Set to initial value */
    score_pElem.innerHTML = 'Score: ' + quiz_score;

    /* Append to #contest */
    document.querySelector('#contest').append(score_pElem);


/* Answer buttons */
    document.querySelectorAll('.multi_choice').forEach(button => {
        button.onclick = () => {
            /* Button clicked stays hover colour */
            button.style.backgroundColor="#4C8100";

            /* All multi_choice buttons are disabled after button click */
            document.querySelectorAll('.multi_choice').forEach(button => {
                button.disabled = true;
            });

            /* Get correct answer from document*/
            const corr_answer = document.querySelector('#correct_answer').dataset.answer;

            /* Test to see if correct_answer has been updated from fetch */
            console.log(corr_answer);

            /* Get contest_id from document */
            var contest_id = document.querySelector('#contest').dataset.id;

            /* Ensure id is integer */
            var id = parseInt(contest_id);

            console.log(id);

            /* Use this next line to increase score using PUT request */
            if (button.dataset.answer == corr_answer)  {

                /* PUT request NOT to supply question index n (set to null/None here) and score_point: true as wish to update score at this point */
                /* Note: the marks around the path are backticks not single quotation marks */
                fetch(`/play_quizAPI/${id}`, {
                    method:'PUT',
                    credentials: 'same-origin',
                    headers:    {
                        'X-CSRFToken': csrftoken,
                    },
                    body: JSON.stringify({
                        question_index: null,
                        score_point: true
                    })
                })
                .then(response => response.json())
                .then(result => {
                    console.log(result);

                    /* GET request to retrieve quiz_score*/
                    fetch(`/play_quizAPI/${id}`,    {
                        method: 'GET',
                        credentials: 'same-origin',
                        headers:    {
                            'X-CSRFToken': csrftoken,
                        }
                    })
                    .then(response => response.json())
                    .then(contest => {

                        /* Get quiz_score from fetch. Global variable */
                        quiz_score = contest.quiz_score;

                        /* Replace innerHTML for quiz_score */
                        score_pElem.innerHTML = 'Score: ' + quiz_score;
                    })
                })
            }

            /* Place tick next to correct answer */
            /* test: console.log('#' + corr_answer);*/
            document.querySelector('#' + corr_answer).innerHTML += " &#10004;";


            /* This section of code fetches the next question and answers */
            /* Create 'Next' button */
            const next_btn = document.createElement("button");
            next_btn.innerHTML = "Next";
            next_btn.className = "btn btn-primary"

            /* Append button to #next_button div. Append is done once for question
            index n less than or equal to zero */
            if (n <= 0) {
                document.querySelector('#next_button').append(next_btn);
            }

            /* next_btn onclick function */
            next_btn.addEventListener('click', function()   {
                /* increase question index by one */
                n += 1;
                /* Test if at the end of the quiz. If beyond last question open quiz_end page */
                if (n <= N-1)   {

                    /* PUT request to supply question index n and score_point: false as don't wish to update score at this point */
                    /* Note: the marks around the path are backticks not single quotation marks */
                    fetch(`/play_quizAPI/${id}`, {
                        method:'PUT',
                        credentials: 'same-origin',
                        headers:    {
                            'X-CSRFToken': csrftoken,
                        },
                        body: JSON.stringify({
                            question_index: n,
                            score_point: false
                        })
                    })
                    .then(response => response.json())
                    .then(result => {
                        console.log(result);

                        /* GET request to retrieve question and answers with index n */
                        fetch(`/play_quizAPI/${id}`,    {
                            method: 'GET',
                            credentials: 'same-origin',
                            headers:    {
                                'X-CSRFToken': csrftoken,
                            }
                        })
                        .then(response => response.json())
                        .then(contest => {
                            console.log(contest.question);
                            console.log(contest.multiple_choice0);

                        /* Pick up id for question and replace innerHTML */
                            document.querySelector('#question').innerHTML = contest.question;
                        /* Pick up span id for multiple choice answer and replace innerHTML */
                            document.querySelector('#answer0').innerHTML = contest.multiple_choice0;
                            document.querySelector('#answer1').innerHTML = contest.multiple_choice1;
                            document.querySelector('#answer2').innerHTML = contest.multiple_choice2;
                            document.querySelector('#answer3').innerHTML = contest.multiple_choice3;
                            /* Add data for correct answer */
                            document.querySelector('#correct_answer').dataset.answer = contest.correct_answer;
                        });
                    /* All multi_choice buttons are reenabled after new question setup.*/
                    /* All multi_choice buttons background colour set to red */
                    document.querySelectorAll('.multi_choice').forEach(button => {
                        button.disabled = false;
                        button.style.backgroundColor="#D73338";
                        })

                    });

                }
                /* If beyond last question open quiz_end page */
                else {
                    /* Remove buttons at quiz_end */
                    document.querySelectorAll('.multi_choice').forEach(button =>    {
                        button.remove();
                    })
                    /* Remove 'Next' button */
                    next_btn.remove();

                    /* Replace Question with quiz_end text. Shows score out of number of questions */
                    document.querySelector('#question').innerHTML = "<h2>Quiz Completed.</h2>" + "<br>" + "<p>You scored: " + quiz_score + " out of " + N + " points.</p>";

                }

            })
        };
    });

    //Code from Django docs to handle CSRF token in Fetch calls
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');
});
