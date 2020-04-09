import os
from flask import Flask, request, redirect, url_for, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# formatting the question by function defined in the class
def format_questions(all_questions):
  formatted_questions = [
    question.format() for question in all_questions
    ]
  return formatted_questions

def paginate_questions(request, all_questions):
  page = request.args.get('page', 1, type=int) # if page is not given than default value is 1
  start = (page-1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions_in_range = all_questions[start:end] # export questions according to the start and end of the current page
  return questions_in_range

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app) # Initialize the CORS
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
  
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  # Get all categories
  @app.route('/categories')
  def get_categories():
    all_categories = Category.query.order_by(Category.id).all() # get all categories
    category_types = [category.type for category in all_categories] # make a list with the categories. Ex.: ['Science', 'History']

    data = {
      'success': True,
      'categories': category_types,
      'total_categories': len(category_types)
    }
    return jsonify(data) # send data in json format
  
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
  # Get all the questions. Default page = 1
  @app.route('/questions')
  def get_questions():
    try:
      all_questions=Question.query.order_by(Question.category_id).all() # order by the category_id
      questions_in_range = paginate_questions(request, all_questions) # get the questions according to the page number
      formatted_questions = format_questions(questions_in_range) # format the questions
      
      all_categories = Category.query.order_by(Category.id).all() # get all categories
      category_types = [category.type for category in all_categories] # make a list with the categories. Ex.: ['Science', 'History']
      
      # if there is no exported questions, that means no questions is found. Through not found error 404
      if len(questions_in_range) == 0:
        abort(404)

      current_category = questions_in_range[0].category # get the category of the 1st question
      current_category_type = current_category.type # get the category type of the 1st question. Ex.: 'Science'

      data = {
        'success': True,
        'questions': formatted_questions,
        'total_questions': len(all_questions),
        'categories': category_types,
        'current_category': current_category_type
      }
      return jsonify(data) # send data in json format
    
    except:
      abort(404)
  
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  # Delete a specific question
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      # if no question is found to delete, that means request unprocessable
      if question is None:
        abort(422)
      
      question.delete()

      data = {
        'success': True,
        'deleted': question_id
      }
      return jsonify(data)
    
    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  # Create a question if the required fields are given
  # In table questions, the question field is unique. Thus same question won't be added twice.
  @app.route('/questions', methods=['POST'])
  def create_question():
    try:
      # Create request:
      # "POST /questions HTTP/1.1" 200 -
      # {'question': '', 'answer': '', 'difficulty': 1, 'category': 1}
      body = request.get_json()
      # print(body)
      question = body.get('question', '')
      answer = body.get('answer', '')
      difficulty = int(body.get('difficulty'))
      category_id = int(body.get('category')) + 1 # frontend sends 0 for category 1, 5 for category 6. Thus id = id + 1
      category=Category.query.get(category_id) # get the category from the category id to use during insertion
      
      if not question or not answer or not difficulty or not category_id:
        abort(400)
      
      else:
        new_question = Question(question = question, answer = answer, difficulty = difficulty, category = category)
        new_question.insert()
        data = {
          'success': True,
          'question_id': new_question.id,
          'question': question,
        }
        return jsonify(data) # send data in json format
    
    except:
      abort(400)
  
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  # Search a question with given searchTerm
  @app.route('/searchquestions', methods=['POST'])
  def search_questions():
    try:
      # Search request:
      # "POST /questions HTTP/1.1" 200 - 
      # {'searchTerm': 'penicilin'}
      body = request.get_json()
      # print(body)
      search_item = body.get('searchTerm', '') # if searchTerm is not defined, keep it empty, to return all questions. Else it will crash.
      all_questions=Question.query.order_by(Question.category_id).filter(Question.question.ilike('%{}%'.format(search_item))).all() # order by the category_id
      questions_in_range = paginate_questions(request, all_questions) # get the questions according to the page number
      formatted_questions = format_questions(questions_in_range) # format the questions
      
      all_categories = Category.query.order_by(Category.id).all() # get all categories
      category_types = [category.type for category in all_categories] # make a list with the categories. Ex.: ['Science', 'History']
      
      # if there is questions in range, return this
      if len(questions_in_range) > 0:
        current_category = questions_in_range[0].category # get the category of the 1st question
        current_category_type = current_category.type # get the category type of the 1st question. Ex.: 'Science'
        data = {
          'success': True,
          'questions': formatted_questions,
          'total_questions': len(all_questions),
          'current_category': current_category_type
        }
      
      # if there is no question in range, return the this
      else:
        data = {
          'success': True,
          'questions': [],
          'total_questions': 0,
          'current_category': category_types[0]
        }
      
      return jsonify(data) # send data in json format
    
    except:
      abort(400)
  
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  # Get questions from a category
  @app.route('/categories/<int:id>/questions')
  def get_questions_from_category(id):
    try:
      id = id + 1 # in frontend the id starts from 0. Ex. to get category 1, frontend sends 0. Thus increment by 1.
      all_questions=Question.query.order_by(Question.id).filter(Question.category_id == id).all() # order by the Question.id
      questions_in_range = paginate_questions(request, all_questions) # get the questions according to the page number
      formatted_questions = format_questions(questions_in_range) # format the questions
      
      all_categories = Category.query.order_by(Category.id).all() # get all categories
      category_types = [category.type for category in all_categories] # make a list with the categories. Ex.: ['Science', 'History']
      
      # if there is no exported questions, that means no questions is found. Through not found error 404
      if len(questions_in_range) == 0:
        abort(404)

      current_category = Category.query.get(id) # get the category from category_id
      current_category_type = current_category.type # get the category type of the 1st question. Ex.: 'Science'
      
      data = {
        'success': True,
        'questions': formatted_questions,
        'total_questions': len(all_questions),
        'current_category': current_category_type
      }
      return jsonify(data) # send data in json format
    except:
      abort(404)


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
  # Get a question to play
  @app.route('/quizzes', methods=['POST'])
  def get_quiz():
    try:
      # Post Body: {'previous_questions': [12, 14, 10], 'quiz_category': {'type': 'Art', 'id': '1'}}
      body = request.get_json()
      previous_questions_ids = body.get('previous_questions', []) # get the list of previous questions
      quiz_category = body.get('quiz_category') # get the dictionary of quiz category
      # get the id from the dictionary of quiz category
      # if the user selects All, the frontend sends 0 as the category id
      # make sure to conver the category id to int
      # To get category 1, frontend sends 0. To get category 2, frontend sends 1. Thus we need to increment the id by 1. Thus id = id + 1
      category_id = int(quiz_category['id'])
      category_id = category_id + 1

      # use print to debug
      # print(body)
      # print(previous_questions)
      # print(category_id)

      # at first get all questions of that category
      all_questions=Question.query.order_by(Question.id).filter(Question.category_id == category_id).all() # order by the Question.id
      
      # some categories may have less than 5 questions.
      # Suppose a category has 2 questions. So, after 2 questions, the game will crash
      # If the length of the previous_questions_ids is equal or greater than the all_questions of this category,
      # that means, all questions from this category is over.
      # Now generate a random question from all_questions which is not previously generated to avoid the crash
      
      if len(previous_questions_ids) >= len(all_questions):
        all_questions = Question.query.order_by(Question.id).all()

      random_question = {}
      # run this while loop while random_question is not empty
      # loop through all_questions and match the id with the previous_questions_ids.
      # if an id is not present in previous_questions_ids, add the corresponding question after formatting as the random_question
      while bool(random_question) is False:
        for question in all_questions:
          if question.id not in previous_questions_ids:
            random_question = question.format()

      data = {
        'success': True,
        'question': random_question,
        'current_category': quiz_category['type']
      }
      return jsonify(data) # send data in json format
    except:
      abort(404)
  
  @app.route('/')
  def index():
    return redirect(url_for('get_questions'))
  
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    data = {
      'success': False,
      'error': 400,
      'message': 'bad request'
    }
    return jsonify(data), 400

  @app.errorhandler(404)
  def not_found(error):
    data = {
      'success': False,
      'error': 404,
      'message': 'resource not found'
    }
    return jsonify(data), 404
  
  @app.errorhandler(405)
  def method_not_allowed(error):
    data = {
      'success': False,
      'error': 405,
      'message': 'method not allowed'
    }
    return jsonify(data), 405

  @app.errorhandler(422)
  def unprocessable(error):
    data = {
      'success': False,
      'error': 422,
      'message': 'unprocessable'
    }
    return jsonify(data), 422
  
  @app.errorhandler(500)
  def internal_server_error(error):
    data = {
      'success': False,
      'error': 500,
      'message': 'internal server error'
    }
    return jsonify(data), 500
  
  return app

    