import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def pagination(selection):
  page = request.args.get('page', 1, type=int)

  start = (page - 1) * QUESTIONS_PER_PAGE
  end  = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]

  current_question = questions[start:end] 

  return current_question


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={'/': {'origins': '*'}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def categorie():
    categories = Category.query.all()
    categorie_dict = {}

    for categorie in categories:
      categorie_dict[f"{categorie.id}"] = categorie.type

    if len(categorie_dict) == 0:
      abort(404)

    return jsonify({
      "success": True,
      "categories": categorie_dict
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
  @app.route('/questions')
  def questions():

    questions = Question.query.all()

    total_question = len(questions)

    question_pagination = pagination(questions)

    categories = Category.query.all()

    categorie_dict = {}

    for categorie in categories:
      categorie_dict[categorie.id] = categorie.type

    if len(question_pagination) == 0:
      abort(404)

    return jsonify({
      "success": True,
      "questions":question_pagination,
      "total_question":total_question,
      "categories":categorie_dict
      })



  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def question_delete(id:int):
    try:
      question = Question.query.filter_by(id=id).one_or_none()

      if question is None:
        abort(404)

      else:
        question.delete()

      return jsonify({
        "success":True,
        "deleted":id
        })
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

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions', methods=['POST'])
  def post_question():

    body = request.get_json()

    # if search term is present
    search_term = body.get('searchTerm')
    if search_term:

        # query the database using search term
        selection = Question.query.filter(
            Question.question.ilike(f'%{search_term}%')).all()

        # 404 if no results found
        if len(selection) == 0:
            abort(404)

        # paginate the results
        paginated = pagination(selection)

        # return results
        return jsonify({
            'success': True,
            'questions': paginated,
            'total_questions': len(Question.query.all())
        })
    # if no search term, create new question
    else:
        # load data from body
        new_question = body.get('question')
        new_answer = body.get('answer')
        new_difficulty = body.get('difficulty')
        new_category = body.get('category')

        # ensure all fields have data
        if any(not item for item in [new_question, new_answer, new_difficulty, new_category]):
            abort(422)

        try:
            # create and insert new question
            question = Question(question=new_question, answer=new_answer,
                                difficulty=new_difficulty, category=new_category)
            question.insert()

            # get all questions and paginate
            selection = Question.query.order_by(Question.id).all()
            current_questions = pagination(selection)

            # return data to view
            return jsonify({
                'success': True,
                'created': question.id,
                'question_created': question.question,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })

        except:
            # abort unprocessable if exception
            abort(422)
     


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions')
  def get_category_questions(id):
    category = Category.query.filter_by(id=id).one_or_none()

    if category is None:
      abort(400)

    selection = Question.query.filter_by(category=category.id).all()

    current_pagination = pagination(selection)

    return jsonify({
      "success":True,
      "questions":current_pagination,
      "total_question":len(Question.query.all()),
      "current_category":category.type
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
  @app.route('/quizzes', methods=['POST'])
  def get_random_quiz_question():
    '''
    Handles POST requests for playing quiz.
    '''

    # load the request body
    body = request.get_json()

    # get the previous questions
    previous = body.get('previous_questions')

    # get the category
    category = body.get('quiz_category')

    # abort 400 if category or previous questions isn't found
    if None in [previous, category]:
        abort(400)

    # load questions all questions if "ALL" is selected
    if category['id'] == 0:
        questions = Question.query.all()
    # load questions for given category
    else:
        questions = Question.query.filter_by(category=category['id']).all()

    # get total number of questions
    total = len(questions)

    # if all questions have been tried, return without question
    # necessary if category has <5 questions
    if len(previous) == total:
        return jsonify({
            'success': True
        })

    # filter questions => get all questions where not in previous
    left_questions = filter(lambda question: question.id not in previous, questions)
    # choice random question
    random_question = random.choice(list(left_questions))

    # return the question
    return jsonify({
        'success': True,
        'question': random_question.format()
    })
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def error_400(error):
    return jsonify({
      "success" : False,
      "error" : 400,
      "message":"Bad request"
      }), 400

  @app.errorhandler(404)
  def error_404(error):
    return jsonify({
      "success": False,
      "error":404,
      "message": "Not Found"
      }), 404

  @app.errorhandler(422)
  def error_422(error):
    return jsonify({
      "success":False,
      "error": 422,
      "message":"Unprocessable"
      }), 422

  @app.errorhandler(500)
  def error_500(error):
    return jsonify({
      "success": False,
      "error":500,
      "message": "Internal Server Error"
      }), 500


  return app

    