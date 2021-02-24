# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

Omit the dropdb command the first time you run tests.

## API Reference

### Getting Started
	* Base URL: Currently this application is only hosted locally. The backend is hosted at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
	* Authentication: This version does not require authentication or API keys.
### Error Handling
Errors are returned as JSON in the following format:

```bash
{
    "success": False,
    "error": 404,
    "message": "Not Found"
}
```

The API will return four types of errors:
	* 400 – Bad Request
	* 404 – Not Found
	* 422 – Unprocessable
	* 500 - Internal Server Error

## Endpoints

#### GET /categories
	* General: Returns a list categories.
	* Sample: `curl http://127.0.0.1:5000/categories`

	
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


### GET /questions
	* General:

		* Returns a list questions.
		* Results are paginated in groups of 10.
		* Also returns list of categories and total number of questions.
	* Sample: curl http://127.0.0.1:5000/questions

	

### DELETE /questions/<int:id>
	* General:
    * Deletes a question by id using url parameters.
		* Returns id of deleted question upon success.

	* Sample: curl http://127.0.0.1:5000/questions/1 -X DELETE
		
```bash
		  {
		      "deleted": 1, 
		      "success": true
		  }
```

### POST /questions
This endpoint either creates a new question or returns search results.
1.If no search term is included in request:
* General:
	* Creates a new question using JSON request parameters.
	* Returns JSON object with newly created question, as well as paginated questions.
* Sample: ```
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question": "Why it is work site udacity?", "answer": "Test answe", "difficulty": 2, "category": "3" }'
```

2.If search term is included in request:
* General:
  * Searches for questions using search term in JSON request parameters.
	* Returns JSON object with paginated matching questions.

* Sample: ``` curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Mahal"}' ```

```bash
  {
    "questions": [
      {
        "answer": "Agra",
        "category": 3,
        "difficulty": 2,
        "id": 15,
        "question": "The Taj Mahal is located in which Indian city?"
      }
    ],
    "success": true,
    "total_questions": 19
  }
```

### GET /categories/<int:id>/questions
* General:
  * Gets questions by category id using url parameters.
	* Returns JSON object with paginated matching questions.

* Sample: ```bash curl http://127.0.0.1:5000/categories/1/questions ```
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
        "answer": "Blood",
        "category": 1,
        "difficulty": 4,
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of what?"
      }
    ],
    "success": true,
    "total_questions": 19
  }
```

### POST /quizzes
- General:

		- Allows users to play the quiz game.
		- Uses JSON request parameters of category and previous questions.
		- Returns JSON object with random question not among previous questions.
- Sample: ```bash curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[20] ,"quiz_category":{"type":"Science","id":"1"}}'```

```bash
  {
    "question": {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    "success": true
  }
```

## Authors
Baxtiyor Eshametov authored the API (__init__.py), test suite (test_flaskr.py), and this README. All other project files, including the models and frontend, were created by [Udacity](https://www.udacity.com/) as a project template for the [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044).
