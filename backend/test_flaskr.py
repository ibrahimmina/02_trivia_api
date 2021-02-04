import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.test import EnvironBuilder

from flaskr import create_app
from models import setup_db, Question, Category
from flask import Flask, url_for

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_name = "trivia"
        self.database_path = "postgres://{}/{}".format('trivia:trivia@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        self.new_question = {
            'question' : 'test_question', 
            'answer' : 'test_answer', 
            'category' : '2', 
            'difficulty' : '5'
        }


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client.get('/api/v1/categories')
        data = json.loads(res.data)
        print (data)
        self.assertEqual(res.status_code, 200)

    def test_getQuestions(self):
        res = self.client.get('/api/v1/questions')
        self.assertEqual(res.status_code, 200)


    def test_submitQuestion(self):
        res = self.client.post('/api/v1/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_questionAction(self):
        res = self.client.delete('/api/v1/questions/26')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
