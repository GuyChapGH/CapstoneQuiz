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



    