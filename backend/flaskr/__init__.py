import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, questions):
    page = request.args.get('page', 1, type = int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in questions]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/": {"origins": "*"}})
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        return response

    @app.route('/')
    def home():
        return jsonify({'success': True}), 200

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        all_categories = {}

        for category in categories:
            all_categories[category.id] = category.type
            
        if len(all_categories) == 0:
            return jsonify({
                'success' : False,
                'categories' : 'no categories found'
            }), 404
        
        return jsonify({
            'success' : True,
            'categories' : all_categories
        }), 200


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)

        if len(current_questions) == 0:
            abort (404)
            
        categories = Category.query.order_by(Category.id).all()
        all_categories = {}

        for category in categories:
            all_categories[category.id] = category.type
     
        return jsonify({
            'success' : True,
            'questions' : current_questions,
            'total_questions' : len(Question.query.all()),
            'categories' : all_categories
        }), 200

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_questions(id):
        question = Question.query.filter(Question.id == id).one_or_none()

        if question is None:
            abort (404)
        
        try:
            question.delete()
        except:
            db.session.rollback()
            abort (422)
        finally:
            db.session.close()
            return jsonify({
                'success' : True,
                'deleted' : id,
            }), 201
        

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions', methods=['POST'])
    def search_or_create_question():
        data = request.get_json()
        if "searchTerm"  in data:
            search_term = data.get("searchTerm")
            search_results = Question.query.filter(Question.question.ilike("%" + search_term + "%"))

            if search_results.count() > 0 :
                current_questions = paginate_questions(request, search_results)
                return jsonify ({
                    'success' : True,
                    'search_term' : search_term,
                    'questions' : current_questions,
                    'total_questions' : len(current_questions)
                })
            else:
                abort (404)

        else:
            data = request.get_json()
            try:
                question = data.get("question").strip()
                answer = data.get("answer").strip()
                difficulty = data.get("difficulty")
                category = data.get("category")
            except:
                abort (500)
        
            if question == "" or answer == "" or difficulty == "" or category == "":
                print("missing")
                abort (400)
            else:
                try:
                    new_question = Question(question = question, 
                                        answer = answer, 
                                        difficulty = difficulty, 
                                        category = category)
                    db.session.add(new_question)
                    db.session.commit()
                except:
                    db.session.rollback()
                    abort(500)
                finally: 
                    print ("closing")
                    db.session.close()
                    return jsonify ({
                        'success' : True,
                        'question' : question,
                        'answer' : answer,
                        'difficulty' : difficulty,
                        'category' : category
                    }), 201

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:id>/questions')
    def get_questions_by_category(id):
        category = Category.query.filter(Category.id == id). one_or_none()
        
        if category is None:
            abort (400)

        questions = Question.query.filter(Question.category == id).all()
        current_questions = paginate_questions(request, questions)

        return jsonify({
            'success' : True,
            'questions' : current_questions,
            'total_questions' : len(questions),
            'current_category' : category.type
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        data = request.get_json()
        quiz_category = data.get("quiz_category")
        previous_questions = data.get("previous_questions")
        quiz_category_id = quiz_category['id']

        if quiz_category_id:
            upcoming_questions = Question.query.filter(Question.id.notin_(previous_questions), Question.category == quiz_category_id).all()
        elif quiz_category_id == 0:
            upcoming_questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
        else:
            abort(404)

        next_question = random.choice(upcoming_questions).format()

        return jsonify({
            'success' : True,
            'question' : next_question,
            'category' : quiz_category_id
        }), 200

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                'error' : 404,
                'success' : False,
                'message' : 'resource not found'
            }),
            404)

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({
                'error' : 422,
                'success' : False,
                'message' : 'unprocessable'
            }),
            422)

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({
                'error' : 400,
                'success' : False,
                'message' : 'bad request'
            }), 
            400)

    @app.errorhandler(500)
    def unprocessable(error):
        return (
            jsonify({
                'error' : 500,
                'success' : False,
                'message' : 'an unexpected error occured, request could not be processed'
            }),
            500)

    return app

