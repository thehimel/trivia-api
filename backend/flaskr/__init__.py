# import os
from flask import Flask, request, redirect, url_for, abort, jsonify
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


# formatting the question by function defined in the class
def format_questions(all_questions):
    formatted_questions = [
        question.format() for question in all_questions]
    return formatted_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Initialize the CORS
    CORS(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    '''
    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, PUT, POST, DELETE, OPTIONS')
        return response

    '''
    GET '/categories'
    - Fetches a dictionary of categories in which the keys are the ids
        and the value is the corresponding string of the category
    - Request Arguments: None
    - Returns: An object with a single key, categories,
        that contains a object of id: category_string key:value pairs.
    {'1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"}
    '''

    def formatted_categories():
        # get all categories
        all_categories = Category.query.order_by(Category.id).all()

        categories = {}
        for category in all_categories:
            categories[category.id] = category.type

        return categories

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''

    # Get all categories
    @app.route('/categories')
    def get_categories():
        # Get the categories as a dictionay of {id: type, id: type}
        categories = formatted_categories()
        total_categories = len(categories)

        data = {
            'success': True,
            'categories': formatted_categories(),
            'total_categories': total_categories
        }

        # send data in json format
        return jsonify(data)

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application,
    you should see questions and categories generated,
    10 questions per page and pagination at the bottom of the screen
    for 3 pages. Clicking on the page numbers should update the questions.
    '''

    # Get all the questions. Default page = 1
    @app.route('/questions')
    def get_questions():
        try:
            # Get the parameter page from the request and by default page=1
            page = request.args.get('page', 1, type=int)

            # Get the questions in the form of Pagination object
            # according to the page number
            questions_in_range_obj = Question.query.order_by(
                Question.category_id).paginate(
                    per_page=QUESTIONS_PER_PAGE, page=page, error_out=True)

            # Get the total number of questions from the Pagination object
            total_questions = questions_in_range_obj.total

            # Get the items from the Pagination object
            questions_in_range = questions_in_range_obj.items

            # format the questions
            formatted_questions = format_questions(questions_in_range)

            # if there is no exported questions,
            # that means no questions is found.
            # Through not found error 404
            if len(questions_in_range) == 0:
                abort(404)

            # get the category of the 1st question
            current_category = questions_in_range[0].category

            # get the category type of the 1st question. Ex.: 'Science'
            current_category_type = current_category.type

            # Get the categories as a dictionay of {id: type, id: type}
            categories = formatted_categories()

            data = {
                'success': True,
                'questions': formatted_questions,
                'total_questions': total_questions,
                'categories': categories,
                'current_category': current_category_type
            }

            # send data in json format
            return jsonify(data)

        except Exception:
            abort(404)

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed. This removal will persist in the database
    and when you refresh the page.
    '''
    # Delete a specific question
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            # if no question is found to delete,
            # that means request unprocessable
            if question is None:
                abort(422)

            question.delete()

            data = {
                'success': True,
                'deleted': question_id
            }

            return jsonify(data)

        except Exception:
            abort(422)

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear
    at the end of the last page of the questions list in the "List" tab.
    '''

    # Create a question if the required fields are given
    # In table questions, the question field is unique.
    # Thus same question will not be added twice.
    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            # Create request:

            """
            "POST /questions HTTP/1.1" 200 -

            {'question': 'What is the closest planet to the Sun?',
            'answer': ' Mercury', 'difficulty': '2', 'category': '1'}
            """

            body = request.get_json()

            # print(body)

            question = body.get('question', '')
            answer = body.get('answer', '')
            difficulty = int(body.get('difficulty'))
            category_id = int(body.get('category'))

            # get the category from the category id to use during insertion
            category = Category.query.get(category_id)

            if not question or not answer or not difficulty or not category_id:
                abort(400)

            else:
                new_question = Question(
                    question=question,
                    answer=answer,
                    difficulty=difficulty,
                    category=category)

                new_question.insert()

                data = {
                    'success': True,
                    'question_id': new_question.id,
                    'question': question,
                }

                # send data in json format
                return jsonify(data)

        except Exception:
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
            # Get the parameter page from the request and by default page=1
            page = request.args.get('page', 1, type=int)

            # Search request:

            """
            "POST /questions HTTP/1.1" 200 -
            {'searchTerm': 'who'}
            """

            body = request.get_json()

            # print(body)

            # if searchTerm is not defined, keep it empty,
            # to return all questions. Else it will crash.
            search_item = body.get('searchTerm', '')

            # Get the questions in the form of Pagination object
            # according to the page number
            # order by the category_id
            questions_in_range_obj = Question.query.order_by(
                Question.category_id).filter(Question.question.ilike(
                    '%{}%'.format(search_item))).paginate(
                        per_page=QUESTIONS_PER_PAGE, page=page, error_out=True)

            # Get the total number of questions from the Pagination object
            total_questions = questions_in_range_obj.total

            # Get the items from the Pagination object
            questions_in_range = questions_in_range_obj.items

            # format the questions
            formatted_questions = format_questions(questions_in_range)

            # if there is questions in range, return this
            if len(questions_in_range) > 0:
                # get the category of the 1st question
                current_category = questions_in_range[0].category

                # get the category type of the 1st question. Ex.: 'Science'
                current_category_type = current_category.type

                data = {
                    'success': True,
                    'questions': formatted_questions,
                    'total_questions': total_questions,
                    'current_category': current_category_type
                }

            # if there is no question in range, return the this
            else:
                data = {
                    'success': True,
                    'questions': [],
                    'total_questions': 0,
                    'current_category': None
                }

            # send data in json format
            return jsonify(data)

        except Exception:
            abort(400)

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''

    # Get questions from a category
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_from_category(category_id):
        try:
            # Get the parameter page from the request and by default page=1
            page = request.args.get('page', 1, type=int)

            # Get the questions in the form of Pagination object
            # according to the page number
            questions_in_range_obj = Question.query.order_by(
                Question.category_id).filter(
                Question.category_id == category_id).paginate(
                    per_page=QUESTIONS_PER_PAGE, page=page, error_out=True)

            # Get the total number of questions from the Pagination object
            total_questions = questions_in_range_obj.total

            # Get the items from the Pagination object
            questions_in_range = questions_in_range_obj.items

            # format the questions
            formatted_questions = format_questions(questions_in_range)

            # if there is no exported questions,
            # that means no questions is found. Through not found error 404
            if len(questions_in_range) == 0:
                abort(404)

            # get the category from category_id
            current_category = Category.query.get(category_id)

            # get the category type of the 1st question. Ex.: 'Science'
            current_category_type = current_category.type

            data = {
                'success': True,
                'questions': formatted_questions,
                'total_questions': total_questions,
                'current_category': current_category_type
            }

            # send data in json format
            return jsonify(data)

        except Exception:
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

            """
            POST Body: {'previous_questions': [12, 14, 10], 'quiz_category':
                {'type': 'Art', 'id': '1'}}
            """

            body = request.get_json()

            # get the list of previous questions
            previous_questions_ids = body.get('previous_questions', [])

            # get the dictionary of quiz category
            quiz_category = body.get('quiz_category')

            # get the id from the dictionary of quiz category
            # if the user selects All, the frontend sends 0 as the category id
            # make sure to convert the category id to int
            category_id = int(quiz_category['id'])

            # use print to debug
            # print(body)
            # print(previous_questions)
            # print(category_id)

            # at first get all questions of that category
            # order by the Question.id
            all_questions = Question.query.order_by(Question.id).filter(
                Question.category_id == category_id).all()

            # some categories may have less than 5 questions.
            # Suppose a category has 2 questions.
            # So, after 2 questions, the game will crash
            # If the length of the previous_questions_ids is equal or greater
            # than the all_questions of this category,
            # that means, all questions from this category is over.
            # Now generate a random question from all_questions
            # which is not previously generated to avoid the crash

            if len(previous_questions_ids) >= len(all_questions):
                all_questions = Question.query.order_by(Question.id).all()

            random_question = {}
            # run this while loop while random_question is not empty
            # loop through all_questions and match the id
            # with the previous_questions_ids.
            # if an id is not present in previous_questions_ids,
            # add the corresponding question after formatting
            # as the random_question
            while bool(random_question) is False:
                for question in all_questions:
                    if question.id not in previous_questions_ids:
                        random_question = question.format()

            data = {
                'success': True,
                'question': random_question,
                'current_category': quiz_category['type']
            }

            # send data in json format
            return jsonify(data)

        except Exception:
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
