import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  db = setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/api/v1/categories')
  @cross_origin()
  def get_categories():
      categorieslist = []    

      categories = Category.query.all()
      for category in categories:
        categorieslist.append(category.type.lower())

      return jsonify({
        "categories":categorieslist,
      })  

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/api/v1/questions',  methods=['GET'])
  @cross_origin()
  def getQuestions():
      page = request.args.get('page', 1, type=int)
      start = (page -1) * 10
      end = start + 10

      questionslist =[]

      categorieslist = []    

      categories = Category.query.all()
      for category in categories:
        categorieslist.append(category.type.lower())
      
      questions = Question.query.all()

      for question in questions:
        questionslist.append({
          'id': question.id,
          'question': question.question,
          'answer': question.answer,
          'category': question.category,
          'difficulty': question.difficulty
        })

      return jsonify({
        "questions":questionslist[start:end], 
        "page": page, 
        "totalQuestions":Question.query.count(),
        "categories":categorieslist,
        "currentCategory": ""
      })  
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/api/v1/questions/<int:question_id>',  methods=['DELETE'])
  @cross_origin()
  def questionAction(question_id):
    try:
      question = Question.query.get(question_id)
      db.session.delete(question)
      db.session.commit()
      return jsonify(success=True)
    except:
      db.session.rollback()
      return jsonify(success=False)
    finally:
      db.session.close()


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/api/v1/questions',  methods=['POST'])
  @cross_origin()
  def submitQuestion():
      questionslist =[]
      request_data = request.get_json()

      search_term = request_data.get("searchTerm")
      search = "%{}%".format(search_term)
      
      questions = Question.query.filter(Question.question.ilike(search)).all()

      for question in questions:
        questionslist.append({
          'id': question.id,
          'question': question.question,
          'answer': question.answer,
          'category': question.category,
          'difficulty': question.difficulty
        })

      return jsonify({
        "questions":questionslist, 
        "totalQuestions":Question.query.count(),
        "currentCategory": ""
      })  
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/api/v1/questions',  methods=['POST'])
  @cross_origin()
  def submitSearch():
      questionslist =[]
      request_data = request.get_json()

      search_term = request_data.get("searchTerm")
      search = "%{}%".format(search_term)
      
      questions = Question.query.filter(Question.question.ilike(search)).all()

      for question in questions:
        questionslist.append({
          'id': question.id,
          'question': question.question,
          'answer': question.answer,
          'category': question.category,
          'difficulty': question.difficulty
        })

      return jsonify({
        "questions":questionslist, 
        "totalQuestions":Question.query.count(),
        "currentCategory": ""
      })  

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/api/v1/categories/<int:category_id>/questions')
  @cross_origin()
  def getByCategory(category_id):
    questionslist =[]
    
    questions = Question.query.filter_by(category=category_id).all()

    currentCategory = Category.query.filter_by(id=category_id).first()

    for question in questions:
      questionslist.append({
        'id': question.id,
        'question': question.question,
        'answer': question.answer,
        'category': question.category,
        'difficulty': question.difficulty
      })

    return jsonify({
      "questions":questionslist, 
      "totalQuestions":len(questionslist),
      "currentCategory": currentCategory.type
    })      


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    