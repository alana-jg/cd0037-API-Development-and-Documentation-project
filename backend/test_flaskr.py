import os
from os.path import join, dirname
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), 'login.env')
load_dotenv(dotenv_path)


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_user = os.getenv('USER')
        self.database_password = os.getenv('PASSWORD')
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(self.database_user, self.database_password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'question' : 'Who invented the light bulb',
            'answer' : 'Thomas Edison',
            'difficulty' : 2,
            'category' : 1
        }

        self.invalid_new_question = {
            'question' : 'Who invented trains',
            'answer' : '',
            'difficulty' : 2,
            'category' : 1
        }

        self.quiz_progress = {
            'previous_questions' : [20],
            'quiz_category' : {
                'id' : 1
            }
        }

        self.invalid_quiz = {
            'previous_questions' : [],
            'quiz_category' : {
                'id' : ''
            }
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_paginated_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_404_beyond_valid_page(self):
        response = self.client().get('/questions?page=1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_delete_questions(self):
        id = 9
        response = self.client().delete('/questions/{}'.format(id))
        data = json.loads(response.data)

        question = Question.query.filter(Question.id == id).one_or_none()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], id)
        self.assertEqual(question, None)

    def test_404_question_deletion_fails(self):
        id = 9000
        response = self.client().delete('/questions/{}'.format(id))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_post_new_question(self):
        response = self.client().post('/questions', json = self.new_question)
        data = json.loads(response.data)

        question = Question.query.filter(Question.question == data['question']).one_or_none()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(question)

    def test_400_missing_field_in_question(self):
        response = self.client().post('/questions', json = self.invalid_new_question)
        data = json.loads(response.data)

        question = Question.query.filter(Question.question == self.invalid_new_question['question']).one_or_none()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
        self.assertEqual(question, None)

    def test_search_question(self):
        searchTerm = "What"
        response = self.client().post('/questions', json = {'searchTerm' : searchTerm})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['search_term'], searchTerm)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_404_search_fails(self):
        searchTerm = "qwertyuiop"
        response = self.client().post('/questions', json = {'searchTerm' : searchTerm})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_questions_for_category(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], 'Science')

    def test_400_get_questions_with_no_valid_category(self):
        response = self.client().get('/categories/1000/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_play_quizzes(self):
        response = self.client().post('/quizzes', json = self.quiz_progress)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(data['category'], self.quiz_progress['quiz_category']['id'])

    def test_404_fail_play_quizzes(self):
        response = self.client().post('/quizzes', json = self.invalid_quiz)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()