import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    # custom lambda helper functions
    check_success = lambda self, response, data: response.status_code == 200 and data['success']
    check_bad_request = lambda self, response, data: response.status_code == 400 and not data['success']
    check_not_found = lambda self, response, data: response.status_code == 404 and not data['success']
    check_unprocessable = lambda self, response, data: response.status_code == 422 and not data['success']


    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}@{}/{}".format('postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
        "question":"Why it is work site udacity?",
        "answer":"Test answer",
        "difficulty":2,
        "category":3
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_question(self):
        res = self.client().get('/questions')

        data = json.loads(res.data)

        self.assertTrue(self.check_success(res, data))

        self.assertTrue(data['questions'])
        self.assertTrue(data['total_question'])

    def test_404_pagination(self):

        res = self.client().get('/questions?page=1000')

        data = json.loads(res.data)

        self.assertTrue(self.check_not_found(res, data))

    def test_delete_question(self):
        question = Question(question=self.new_question['question'], answer=self.new_question['answer'],
                            difficulty=self.new_question['difficulty'], category=self.new_question['category'])

        question.insert()
        delete_question_test = Question.query.filter(Question.id == question.id).one_or_none()

        res = self.client().delete(f'question/{question.id}')

        data = json.loads(res.data)

        real_delete_question = Question.query.filter(Question.id==question.id).one_or_none()

        self.assertTrue(self.check_success(res, data))

        self.assertTrue(data['deleted'], question.id)

        self.assertTrue(delete_question_test)
        self.assertEqual(real_delete_question, None)

    def test_create_question(self):
        # create question

        res = self.client().post(f'/questions', json=self.new_question)
        data = json.loads(res.data)

        # check success
        self.assertTrue(self.check_success(res, data))

        # check created
        self.assertTrue(data['created'])
        # get created question
        question = Question.query.get(data['created'])
        self.assertTrue(question)

    def test_422_question_creation_fails(self):
        # fail create question

        questions_before = Question.query.count()
        # request to api and convert json to dict
        res = self.client().post(f'/questions', json={'you': 'need', 'to be': '422'})
        data = json.loads(res.data)

        # check unprocessable
        self.assertTrue(self.check_unprocessable(res, data))

        # questions count after create
        questions_after = Question.query.count()
        # check count questions before == after
        self.assertEqual(questions_before, questions_after)

    def test_search_questions(self):
        # search question

        res = self.client().post('/questions', json={'searchTerm': 'Mahal'})

        # load response data
        data = json.loads(res.data)

        # check success
        self.assertTrue(self.check_success(res, data))

        # check results count == 1
        self.assertEqual(len(data['questions']), 1)

    def test_404_search_questions_fails(self):
        # search not found

        res = self.client().post('/questions', json={'searchTerm': 'you need to be 404'})

        # load response data
        data = json.loads(res.data)

        # check not found
        self.assertTrue(self.check_not_found(res, data))

    def test_get_questions_by_category(self):
        # get question by categoty

        res = self.client().get('/categories/1/questions')

        # load response data
        data = json.loads(res.data)

        # check success
        self.assertTrue(self.check_success(res, data))

        # check that questions are returned (len != 0)
        self.assertNotEqual(len(data['questions']), 0)

        # check that current category returned is science
        self.assertEqual(data['current_category'], 'Science')

    def test_400_if_questions_by_category_fails(self):
        # bad request

        res = self.client().get('/categories/400/questions')

        # load response data
        data = json.loads(res.data)

        # check bad request
        self.assertTrue(self.check_bad_request(res, data))

    def test_play_quiz_game(self):
        # get next question

        res = self.client().post('/quizzes',
                                 json={'previous_questions': [1, 2],
                                       'quiz_category': {'type': 'Science', 'id': '1'}
                                       }
                                 )

        # load response data
        data = json.loads(res.data)

        # check success
        self.assertTrue(self.check_success(res, data))

        # check that a question is returned
        self.assertTrue(data['question'])

        # check that the question returned is in correct category
        self.assertEqual(data['question']['category'], 1)

        # check that question returned is not on previous q list
        self.assertNotEqual(data['question']['id'], 1)
        self.assertNotEqual(data['question']['id'], 2)

    def test_400_play_quiz_fails(self):
        # bad request

        res = self.client().post('/quizzes', json={'you': 'need', 'to be': '400'})

        # load response data
        data = json.loads(res.data)

        # check bad request
        self.assertTrue(self.check_bad_request(res, data))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()