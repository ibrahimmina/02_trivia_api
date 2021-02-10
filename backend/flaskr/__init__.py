import os
from flask import Flask, request, abort, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  app = Flask(__name__)
  db = setup_db(app)
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response

  @app.route('/api/v1/categories')
  @cross_origin()
  def get_categories():
      categorieslist = []    

      categories = Category.query.all()

      if len(categories) == 0:
        abort(404)
        
      for category in categories:
        categorieslist.append(category.type.lower())

      return jsonify({
        "categories":categorieslist,
      })  

  @app.route('/api/v1/questions',  methods=['GET'])
  @cross_origin()
  def getQuestions():
      page = request.args.get('page', 1, type=int)
      start = (page -1) * 10
      end = start + 10
      questionslist =[]
      categorieslist = []    
      categories = Category.query.all()
      if len(categories) == 0:
        abort(404) 
      for category in categories:
        categorieslist.append(category.type.lower())      
      questions = Question.query.all()
      if len(questions) == 0:
        abort(404)      
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
        "total_questions":Question.query.count(),
        "categories":categorieslist,
        "current_category": ""
      })  

  @app.route('/api/v1/questions/<int:question_id>',  methods=['DELETE'])
  @cross_origin()
  def questionAction(question_id):
    try:
      question = Question.query.get(question_id)
      db.session.delete(question)
      db.session.commit()
      return jsonify(success=True,questionId=question_id)
    except:
      db.session.rollback()
      return jsonify(success=False,questionId=question_id)
    finally:
      db.session.close()

  @app.route('/api/v1/questions',  methods=['POST'])
  @cross_origin()
  def submitQuestion():
    questionslist =[]
    request_data = request.get_json()
    if ("question" not in request_data or "answer" not in request_data or "category" not in request_data or "difficulty" not in request_data):
      abort(422) 
    try:
      category = Category.query.filter_by(type=request_data.get("category").capitalize()).first()
      question = Question(request_data.get("question"), request_data.get("answer"), category.id, request_data.get("difficulty"))
      question.insert()           
      return jsonify(success=True,id=question.id)
    except:
      db.session.rollback()
      return jsonify(success=False)
    finally:
      db.session.close()    

  @app.route('/api/v1/questions/search',  methods=['POST'])
  @cross_origin()
  def submitSearch():
      questionslist =[]


      if (request.get_json() is None):
        abort(422) 

      request_data = request.get_json()

      if ("searchTerm" not in request_data):
        abort(422) 

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

  @app.route('/api/v1/categories/<string:category_type>/questions')
  @cross_origin()
  def getByCategory(category_type):
    questionslist =[]
    category = Category.query.filter_by(type=category_type.capitalize()).first()      
    if (bool(category) == False):
      abort(422)       
    questions = Question.query.filter_by(category=category.id).all()    
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
      "total_questions":len(questionslist),
      "current_category": category.type
    })      

  @app.route('/api/v1/quizzes' , methods=['POST'])
  @cross_origin()
  def getNextQuestion():
    currentQuestion = {}
    request_data = request.get_json()
    if (request.get_json() is None):
      abort(422)     
    previousquestionslist = request_data.get("previous_questions")
    quiz_category = request_data.get("quiz_category")    
    category_type =  quiz_category["type"]
    if (category_type == "click"):
      questions = Question.query.all()    
    else:
      category = Category.query.filter_by(type=category_type.capitalize()).first()
      if (bool(category) == False):
        abort(422)       
      questions = Question.query.filter_by(category=category.id).all()
    for question in questions:
      if (question.id not in previousquestionslist):
        previousquestionslist.append(question.id)
        currentQuestion = {
          'id': question.id,
          'question': question.question,
          'answer': question.answer,
          'category': question.category,
          'difficulty': question.difficulty
        }
        break

    if (len(currentQuestion) == 0):
      return jsonify({
        "success": True
      })
    return jsonify({
      "showAnswer": False, 
      "previousQuestions":previousquestionslist,
      "question": currentQuestion,
    })      

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False, 
          "error": 404,
          "message": "Not found"
          }), 404
  
  @app.errorhandler(422)
  def not_found(error):
      return jsonify({
          "success": False, 
          "error": 422,
          "message": "Not found"
          }), 422     
  
  return app

    