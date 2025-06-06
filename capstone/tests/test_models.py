from django.test import TestCase

from capstone.models import User, Question

# Create your tests here.

class QuestionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        # Create user
        test_user1 = User.objects.create_user(username = 'testuser1', password='testpassword')
        test_user1.save()
        
        Question.objects.create(user=test_user1, content='Is this a test question?', answer0='Yes', answer1='No', answer2='No', answer3='No', correct_answer='answer0')

    def test_answer0_max_length(self):
        question = Question.objects.get(id=1)
        max_length = question._meta.get_field('answer0').max_length
        self.assertEqual(max_length, 30)

    def test_answer1_max_length(self):
            question = Question.objects.get(id=1)
            max_length = question._meta.get_field('answer1').max_length
            self.assertEqual(max_length, 30)

    def test_answer2_max_length(self):
        question = Question.objects.get(id=1)
        max_length = question._meta.get_field('answer2').max_length
        self.assertEqual(max_length, 30)

    def test_answer3_max_length(self):
        question = Question.objects.get(id=1)
        max_length = question._meta.get_field('answer3').max_length
        self.assertEqual(max_length, 30)

    def test_correct_answer_max_length(self):
        question = Question.objects.get(id=1)
        max_length = question._meta.get_field('correct_answer').max_length
        self.assertEqual(max_length, 30)
    
    def test_object_name_is_question_content(self):
        question = Question.objects.get(id=1)
        expected_object_name = f'Question: {question.content}'
        self.assertEqual(str(question), expected_object_name)