from django.test import TestCase
from django.urls import reverse

from capstone.models import User, Question, Quiz, Contest

import json

# Create your tests here.

class PlayQuizAPIViewDatabaseTest(TestCase):
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

    def test_put_request_increases_quiz_score_by_1_when_logged_in(self):
        # Login and get response
        login = self.client.login(username = 'testuser1', password='testpassword')
        
        put_data = {"question_index": None, "score_point": True}

        contest_id = Contest.objects.all().last().id
        response = self.client.put(reverse("play_quizAPI", args=(contest_id,)), data=put_data, content_type='application/json')

        # Check put request increases quiz_score by one point

        contest = Contest.objects.get(id=1)
        expected_score = "1"
        self.assertEqual(contest.q_score(), expected_score)

    def test_put_request_with_index_n_followed_by_get_request_returns_all_content_data_when_logged_in(self):
        # Login and get response
        login = self.client.login(username = 'testuser1', password='testpassword')
        
        # Set index n to zero
        put_data = {"question_index": 0, "score_point": False}

        # Send put request
        contest_id = Contest.objects.all().last().id
        put_response = self.client.put(reverse("play_quizAPI", args=(contest_id,)), data=put_data, content_type='application/json')

        # Send get request
        get_response = self.client.get(reverse("play_quizAPI", args=(contest_id,)))

        # Decode json portion of JsonResponse found in 'content'
        get_response_content = json.loads(get_response.content.decode())
        
        # Check response matches expected values 
        self.assertEqual(get_response_content['question'], "Is this a test question?")

        self.assertEqual(get_response_content['multiple_choice0'], 'Yes') 
        self.assertEqual(get_response_content['multiple_choice1'], 'No') 
        self.assertEqual(get_response_content['multiple_choice2'], 'No') 
        self.assertEqual(get_response_content['multiple_choice3'], 'No') 

        self.assertEqual(get_response_content['correct_answer'], 'answer0')

        self.assertEqual(get_response_content['quiz_score'], '0')         



    
        