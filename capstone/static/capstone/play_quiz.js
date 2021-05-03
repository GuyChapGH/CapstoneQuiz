document.addEventListener('DOMContentLoaded', () => {
    /* Define question index. From 0 to N-1. Where N is the number of questions in the quiz.*/
    var n=0;
    document.querySelectorAll('.multi_choice').forEach(button => {
        button.onclick = () => {
            /* Button clicked stays hover colour */
            button.style.backgroundColor="#4C8100";

            /* All multi_choice buttons are disabled after button click */
            document.querySelectorAll('button').forEach(button => {
                button.disabled = true;
            });

            /* Get correct answer from document*/
            const corr_answer = document.querySelector('#correct_answer').dataset.answer;

            /* Use this next line to increase score using PUT request */
            /* if (button.dataset.answer == corr_answer)  {
                alert('Correct Answer!'+ corr_answer);
            }
            else {
                alert('Wrong Answer!' + corr_answer);
            } */

            /* Place tick next to correct answer */
            /* test: console.log('#' + corr_answer);*/
            document.querySelector('#' + corr_answer).innerHTML += " &#10004;";


            /* This section of code fetches the next question and answers */
            /* Create 'Next' button */
            const next_btn = document.createElement("button");
            next_btn.innerHTML = "Next";

            /* Append button to #contestant paragraph */
            document.querySelector('#contestant').append(next_btn);

            /* next_btn onclick function */
            next_btn.addEventListener('click', function()   {
                /* increase question index by one */
                n += 1;

                /* Get contestant_id from document */
                const contestant_id = document.querySelector('#contestant').dataset.id;

                /* Ensure id is integer */
                const id = parseInt(contestant_id);
                /* const id = 4; */

                console.log(id);

                /* PUT request to get next question and answers for index n */
                /* Note: the marks around the path are backticks not single quotation marks */
                fetch(`/play_quizAPI/${id}`, {
                    method:'PUT',
                    body: JSON.stringify({
                        question_index: n
                    })
                })
                .then(response => response.json())
                .then(question => {
                    console.log(question);
                });
            })

            /* test: console.log(button.dataset.answer); */
        };
    });
});
