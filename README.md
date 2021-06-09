# Capstone Quiz Application

## Introduction
The Capstone Quiz Application is an user-defined multiple-choice quiz application. 

The user submits one or several multiple-choice questions with a correct answer or selects from the questions already held in the database. The user can then group together a number of questions to define a quiz with an unique name. 

To play the quiz, the name is selected and the quiz is answered by using the onscreen buttons.

To review quiz results of previous contestants, the 'Results' link is selected and, for the chosen quiz, the results of the last five quiz contestants are shown as a barchart. 

The Capstone Quiz Application is inspired by the [Kahoot!](https://kahoot.com) game-based learning platform.

## Distinctiveness and Complexity
This project has three models (not including the User model). They build on each other, with the Quiz model including the Question model and the Contestant model including the Quiz model. This structure is distinctive and different to anything seen in the course.

The complexity of the application is best demonstrated by the 'play_quiz.js' JavaScript file. 

Once a quiz has been selected, this file controls the progress through the quiz. The 'Next' button and fetch calls take the user through each question in the quiz. The score responds to clicking on an answer button. The answer selected is checked against the correct answer and the score is updated by another fetch call. There is one point available per question and after the user has selected their answer, the correct answer is displayed on screen with a 'tick'. 

The number of questions in the quiz is also established and the number of points scored out of the total available is shown at the end of the quiz.
## Files

### forms.py
### models.py
The User model is 

The Question model is 

The Quiz model is

The Contestant model was originally designed to have one contestant object for each user and reused for each quiz played. Instead the application was implemented with a new contestant object for each quiz played. This was seeen to be more natural but required that the 'first_quiz' be accessed for each object as it was previously a many-to-many field. A future improvement would be to redesign this field as a many-to-one (ForeignKey) relationship.


### urls.py
### views.py

### play_quiz.js
### results_display.js
### styles.css

### create_question.html
### create_quiz.html
### index.html
### layout.html
### play_quiz.html
### quiz_select.html
### results_display.html
### results_select.html

## How to run the application

## Specification

### Define multiple choice questions

### Define quiz by selecting a group of questions

### Play quiz

**Select quiz**

**Play quiz**

**End quiz**

### Quiz results

**Select results**

**Display results**
