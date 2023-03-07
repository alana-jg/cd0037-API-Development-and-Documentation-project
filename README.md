# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game. The application allows you to:

1. Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.



## Dependencies

### Backend 
1. Install required software:
  - Python 3.7
  - Virtual Environement
  - Postgres

2. Set up and populate the database:
With Postgres running, create a trivia database:
`createdb trivia`
From the backend folder in terminal, Populate the database using the trivia.psql file provided:
`psql trivia < trivia.psql`

3. Install dependencies:
`pip install -r requirements.txt`

4. Run the application
`export FLASK_APP=flaskr
export FLASK_ENV=development
flask run`

The application is run on `http://127.0.0.1:5000/` by default

### Frontend
1. Install Node and NPM
2. Install dependencies by navigating to the frontend folder and running:
`npm install`

To start the app in development mode, navigate to the /frontend directory and run:
`npm start`

By default, the frontend will run on `localhost:3000`.

## API Reference
### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:
```bash
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return four error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 500: An unexpected error occured

### Endpoints

#### GET /categories

- General
  - Returns a list of categories
- Sample `curl http://127.0.0.1:5000/categories`
```bash
{ 
  "categories": {
          "1": "Science",
          "2": "Art",
          "3": "Geography",
          "4": "History",
          "5": "Entertainment",
          "6": "Sports"
        },
        "success": true
}
```

#### GET /questions

- General
  - Returns a list of questions, categories and total number of questions
  - Results are paginated in groups of 10
-  Sample `curl http://127.0.0.1:5000/questions`

```bash
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 21
}
```

#### DELETE /questions

- General
  - Deletes a question by given ID if it exists
-  Sample `curl -X DELETE http://127.0.0.1:5000/questions/1`

```bash
{
  "deleted": 1,
  "success": true
}
```

### POST /questions
Will either search for questions or create a new question

1. If search term is included:
- General
  - Searches for questions with at least partial match to search query
  - Results are paginated in groups of 10
- Sample `curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"searchTerm": "Tom"}'`
```bash
{
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ], 
  "search_term": "Tom", 
  "success": true, 
  "total_questions": 1
}
```

2. If search term is not included:
- General
  - Creates a new question if 'question', 'answer', 'difficulty' and 'category' are valid fields passed in to the JSON request
- Sample `curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question":"Who was the first Disney princess?", "answer":"Snow White", "difficulty":"2", "category":"4"}'`
```bash
{
  "answer": "Snow White", 
  "category": "4", 
  "difficulty": "2", 
  "question": "Who was the first Disney princess?", 
  "success": true
}
```

### GET /categories/{category_id}/questions
- General
  - Returns all questions in a selected category
  - Results are paginated in groups of 10
- Sample `curl http://127.0.0.1:5000/categories/1/questions`
```bash
{
  "current_category": "Science", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Dogs", 
      "category": 1, 
      "difficulty": 1, 
      "id": 24, 
      "question": "What's the best animal?"
    }, 
    {
      "answer": "Marie Curie", 
      "category": 1, 
      "difficulty": 2, 
      "id": 29, 
      "question": "Who was the first woman to win a Nobel Prize?"
    }
  ], 
  "success": true, 
  "total_questions": 4
}
```

### POST /quizzes
- General
  - Gets questions to play the quiz, taking parameters of category, if selected, and previous questions to prevent duplicates
  - Questions are selected randomly from questions not previously in the quiz
- Sample `curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions": [27], "quiz_category": {"type": "Science", "id": "1"}}'`
```bash
{
  "category": "1", 
  "question": {
    "answer": "Marie Curie", 
    "category": 1, 
    "difficulty": 2, 
    "id": 29, 
    "question": "Who was the first woman to win a Nobel Prize?"
  }, 
  "success": true
}
```

## Authors
Alana Graham authored the API `__init__.py`, test suite `test_flaskr.py` and README file. All other files were created by Udacity and provided as part of the Full Stack Web Developer Nanodegree.
