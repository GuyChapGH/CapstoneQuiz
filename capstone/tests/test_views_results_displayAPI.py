from django.test import TestCase
from django.urls import reverse

from capstone.models import User, Question, Quiz, Contest

import json

# Create your tests here.

class ResultsDisplayAPIViewDatabaseTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username = 'testuser1', password='testpassword')
        test_user1.save()

        # Create question
        test_question = Question.objects.create(user=test_user1, content='Is this a test question?', answer0='Yes', answer1='No', answer2='No', answer3='No', correct_answer='answer0')

        test_question.save()

        # Create quiz
        test_quiz = Quiz.objects.create(user=test_user1, quiz_name='test_quiz1')
        test_quiz.questions.add(test_question)
        test_quiz.save()

        # Create contest
        test_contest = Contest.objects.create(user=test_user1, quiz=test_quiz)
        test_contest.save()

    def test_get_request_returns_all_content_data_when_logged_in(self):
        # Login and get response
        login = self.client.login(username = 'testuser1', password='testpassword')

        # Send get request
        quiz_id = Quiz.objects.all().first().id
        get_response = self.client.get(reverse("results_displayAPI", args=(quiz_id,)))

        # Decode json portion of JsonResponse found in 'content'
        get_response_content = json.loads(get_response.content.decode())
        
        # Check response matches expected values 
        self.assertEqual(get_response_content['labels'], ['testuser1'])

        self.assertEqual(get_response_content['data'], [0]) 
         