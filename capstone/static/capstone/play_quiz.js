document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('button').forEach(button => {
        button.onclick = () => {
            /* Button clicked stays hover colour */
            button.style.backgroundColor="#4C8100";

            /* All buttons are disabled after button click */
            document.querySelectorAll('button').forEach(button => {
                button.disabled = true;
            });

            /* Test for correct answer */
            const corr_answer = document.querySelector('#correct_answer').dataset.answer
            if (button.dataset.answer == corr_answer)  {
                alert('Correct Answer!'+ corr_answer);
            }
            else {
                alert('Wrong Answer!' + corr_answer);
            }

            /* Place tick next to correct answer */
            console.log('#' + corr_answer);
            document.querySelector('#' + corr_answer).innerHTML += " &#10004;"; 


            console.log(button.dataset.answer);
        };
    });
});
