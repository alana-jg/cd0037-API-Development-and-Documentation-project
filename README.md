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

- Returns a list of categories
- Sample `curl http://127.0.0.1:5000/categories`
```bash
{ "categories" : {
          "1": "Science",
          "2": "Art",
          "3": "Geography",
          "4": "History",
          "5": "Entertainment",
          "6": "Sports"
        },
        "success" : true
}`
```
