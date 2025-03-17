# Capstone Quiz Application
## Notes

This began as a copy of the CS50wPFP repository. 
It was set up to allow for the refactoring of the code and the ultimate deployment to the web.

## Introduction
The Capstone Quiz Application is an user-defined multiple-choice quiz application. 

The user submits one or several multiple-choice questions with a correct answer or selects from the questions already held in the database. The user can then group together a number of questions to define a quiz with an unique name. 

To play the quiz, the name is selected and the quiz is answered by using the onscreen buttons.

To review quiz results of previous contestants, the 'Results' link is selected and, for the chosen quiz, the results of the last five quiz contestants are shown as a barchart. 

The Capstone Quiz Application is inspired by the [Kahoot!](https://kahoot.com) game-based learning platform.

## Distinctiveness and Complexity
This project has three models (not including the User model). They build on each other, with the Quiz model including the Question model and the Contestant model including the Quiz model. This structure is distinctive and different to anything seen in the course.

The complexity of the application is best demonstrated by the 'play_quiz.js' JavaScript file. 

Once a quiz has been selected, this file controls the progress through the quiz. It responds to clicking on an answer button. The answer selected is checked against the correct answer and the score is updated by a fetch call. There is one point available per question. After the user has selected their answer, the correct answer is displayed on screen with a 'tick'. The 'Next' button and fetch calls take the user through each question in the quiz. The question index is tested against the number of questions in the quiz at each step. At the end of the quiz, the number of points scored out of the total available is shown.

## Files

### forms.py
This file contains three ModelForm classes: `QuestionCreateForm`, `QuizCreateForm` and `ContestantSelectForm`. This makes use of the Django ability to create a Form class from a Django model. There is one Form class declared: `ResultsSelectForm`. Django's form functionality simplifies and automates form processing including form validation.

### models.py
In this file we have the `User` model, used for managing login/logout and register. The `Question` model, that captures the multiple-choice questions. The `Quiz` model that groups questions together and the `Contestant` model used for playing the quiz.

The `Contestant` model was originally designed to have one contestant object for each user and to be reused for each quiz played. Instead, the application was implemented with a new contestant object for each quiz played. This was seen to be more natural but required that the 'first_quiz' be accessed for each object as it was previously a many-to-many field. A future improvement would be to redesign this field to have a many-to-one (ForeignKey) relationship. 

Nine methods are declared for the `Contestant` model. These support the 'play_quiz' and 'play_quizAPI' views and are used to play the quiz. 

### urls.py
The paths are defined in this file. Seven paths reference 'index', 'create_question', 'create_quiz', 'quiz_select', 'play_quiz', 'results_select' and 'results_display' views. Two paths are for the API routes(views): 'play_quizAPI' and 'results_displayAPI'. And three are related to the user functionality views.

### views.py
This file contains twelve Django views. 

The 'index' view simply renders the index html page which describes how to use the application. 

The 'create_question' view takes input from the `QuestionCreateForm` to populate the database with questions. The form and the last saved question are displayed by the associated template.

The 'create_quiz' view takes input from the `QuizCreateForm` to group together questions into a quiz and store with an unique quiz name.

Data from the `ContestantSelectForm` is used by the 'quiz_select' view to initiate playing the quiz.

The 'play_quiz' view uses the contestant_id to call up the Contestant object with the details of the chosen quiz. The first question of the quiz is rendered in the associated template.

As the quiz progresses fetch calls are used, index n, to call up the nth question and multiple-choice answers. This is handled by the 'play_quizAPI' view. The view uses the methods defined in the Contestant model to access these question and answer details and is also used to update the quiz score.

The 'results_select' view takes input from the `ResultsSelectForm` to get the id of the results in which the user is interested.

The last five quiz results for the given id are handled by the 'results_display' view and they are rendered in the asssociated template.

In 'results_displayAPI' the quiz results are sampled in a format that can be rendered into a barchart using the [Chart.js](https://www.chartjs.org) data visualisation library.

The remaining three views: 'login_view', 'logout_view' and 'register' all handle the user access to the application and are unchanged from CS50W 2020 Project 4.

### play_quiz.js
This file controls the progress through the quiz using JavaScript. The content is as follows:

    1. Define 'n', the question index. Define 'N', the number of questions in the quiz. Define 'quiz_score' and display on quiz page.
    2. Answer buttons, onclick function.
    3. If correct answer clicked,
        1. fetch request to increase 'quiz_score',
        2. update 'quiz_score' on quiz page.
    4. Add 'tick' to correct answer on quiz page.
    5. Create 'Next' button onclick function, if clicked,
        1. increase 'n' by one,
        2. test if 'n' less than or equal to 'N-1' (still within quiz),
          1. fetch next question and answers,
          2. update question and answer buttons on quiz page.
        else,
          1. go to 'quiz_end'. Remove answer buttons, remove 'Next' button and show score out of the number of points available.
    6. Block of code to handle CSRF-token in fetch calls.

### results_display.js
This file handles the generation of the barchart from results data using JavaScript and the data visualisation library, [Chart.js](https://www.chartjs.org). The content is as follows:

    1. Get 'quiz_id'.
    2. Block of code to handle CSRF-token in fetch calls.
    3. Fetch barchart data and labels for given 'quiz_id'.
    4. Draw barchart using library code.

### styles.css
This file contains CSS styling for 'create_question.html', 'create_quiz.html' and 'play_quiz.html' templates.

### create_question.html
This template renders the `QuestionCreateForm` and the last saved question.

### create_quiz.html
This template renders the `QuizCreateForm`.

### index.html
This file contains text instructions for using the application.

### layout.html
This is the base template extended in all the template files. It provides the navigation bar and loads [Bootstrap](https://getbootstrap.com) and [Chart.js](https://www.chartjs.org) libraries and the 'styles.css' file.

### play_quiz.html
This template works in conjunction with the 'play_quiz.js' file. It renders the first question and answers of the quiz and holds data used by the JavaScript file.

### quiz_select.html
This template renders the `ContestantSelectForm`.

### results_display.html
Quiz results are rendered in this template and it provides a container for the barchart 'canvas' used by 'results_display.js'.

### results_select.html
The `ResultsSelectForm` is rendered in this template.

### login.html and register.html
These two templates contain forms for handling user functionality and are unchanged from CS50W 2020 Project 4.

## How to run the application
No additional Python packages are required to run this application. To run, use `$ python manage.py runserver` in a suitable Python/ Django virtual environment.

## Additional information
The mobile responsive Grid System, Buttons and Navigation Bar are provided by the [Bootstrap](https://getbootstrap.com) framework. The data visualisation library used in the application is [Chart.js](https://www.chartjs.org). They are both loaded automatically from links in the 'layout.html' file.
