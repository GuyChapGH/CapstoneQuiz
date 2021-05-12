document.addEventListener('DOMContentLoaded', () => {
    /* Define question index. From 0 to N-1. Where N is the number of questions in the quiz.*/
    var n = 0;
    /* Define N, the number of questions in the quiz */
    /* Get value of N from html page. First get value of N from count() in play_quiz route */
    /* var N = 10; */
    var N = document.querySelector('#number_questions').dataset.number_questions;

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

            /* Get contestant_id from document */
            var contestant_id = document.querySelector('#contestant').dataset.id;

            /* Ensure id is integer */
            var id = parseInt(contestant_id);

            console.log(id);

            /* Use this next line to increase score using PUT request */
            if (button.dataset.answer == corr_answer)  {
                /* alert('Correct Answer!'+ corr_answer); */
                /* PUT request NOT to supply question index n (set to null/None here) and score_point: true as wish to update score at this point */
                /* Note: the marks around the path are backticks not single quotation marks */
                fetch(`/play_quizAPI/${id}`, {
                    method:'PUT',
                    body: JSON.stringify({
                        question_index: null,
                        score_point: true
                    })
                })
                .then(response => response.json())
                .then(result => {
                    console.log(result);
                });
            }
            /* else {
                alert('Wrong Answer!' + corr_answer);
            } */

            /* Place tick next to correct answer */
            /* test: console.log('#' + corr_answer);*/
            document.querySelector('#' + corr_answer).innerHTML += " &#10004;";


            /* This section of code fetches the next question and answers */
            /* Create 'Next' button */
            const next_btn = document.createElement("button");
            next_btn.innerHTML = "Next";

            /* Append button to #contestant paragraph. Append is done once for question
            index n less than or equal to zero */
            if (n <= 0) {
                document.querySelector('#contestant').append(next_btn);
            }
            /* console.log("n = " + n); */
            /* next_btn onclick function */
            next_btn.addEventListener('click', function()   {
                /* increase question index by one */
                n += 1;
                /* Test if at the end of the quiz. If beyond last question open quiz_end page */
                if (n <= N-1)   {

                    /* Get contestant_id from document */
                    /* REPLACED by var declaration on line 26 */
                    /* const contestant_id = document.querySelector('#contestant').dataset.id; */

                    /* Ensure id is integer */
                    /* const id = parseInt(contestant_id); */
                    /* const id = 4; */

                    console.log(id);

                    /* PUT request to supply question index n and score_point: false as don't wish to update score at this point */
                    /* Note: the marks around the path are backticks not single quotation marks */
                    fetch(`/play_quizAPI/${id}`, {
                        method:'PUT',
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
                            method: 'GET'
                        })
                        .then(response => response.json())
                        .then(contestant => {
                            console.log(contestant.question);
                            console.log(contestant.multiple_choice0);

                        /* Pick up id for question and replace innerHTML */
                            document.querySelector('#question').innerHTML = contestant.question;
                        /* Pick up span id for multiple choice answer and replace innerHTML */
                            document.querySelector('#answer0').innerHTML = contestant.multiple_choice0;
                            document.querySelector('#answer1').innerHTML = contestant.multiple_choice1;
                            document.querySelector('#answer2').innerHTML = contestant.multiple_choice2;
                            document.querySelector('#answer3').innerHTML = contestant.multiple_choice3;
                            /* Add data for correct answer */
                            document.querySelector('#correct_answer').dataset.answer = contestant.correct_answer;
                        });
                    /* All multi_choice buttons are reenabled after new question setup.*/
                    /* All multi_choice buttons background colour set to red */
                    document.querySelectorAll('.multi_choice').forEach(button => {
                        button.disabled = false;
                        button.style.backgroundColor="#D73338";
                        /* button.style:hover.backgroundColor="#4C8100"; */
                        })

                    });

                }
                /* If beyond last question open quiz_end page */
                else {
                    /* This call to open new page is not working. URL helper doesn't work in JavaScript??*/
                    /* document.location.href = "{% url 'index' %}"; */
                    /* This alternative works...*/
                    /* document.location.href = "http://localhost:8000/"; */

                    /* Remove buttons at quiz_end */
                    document.querySelectorAll('.multi_choice').forEach(button =>    {
                        button.remove();
                    })
                    /* Remove 'Next' button */
                    next_btn.remove();
                    /* Replace Question with quiz_end text. TODO add score out of number of questions */
                    document.querySelector('#question').innerHTML = "<h2>Quiz Completed.</h2>" + "<br>" + "<p>You scored: " + " out of " + N + " points.</p>";

                }

            })

                /* test: console.log(button.dataset.answer); */
        };
    });
});
