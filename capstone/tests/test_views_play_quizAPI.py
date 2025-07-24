from django.test import TestCase
from django.urls import reverse

from capstone.models import User, Question, Quiz, Contest

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
    
        