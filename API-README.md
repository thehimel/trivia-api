## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Features
* Endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint returns a list of questions, number of total questions, current category, categories.
* Endpoint to handle GET requests for all available categories.
* Endpoint to DELETE question using a question ID.
* Endpoint to POST a new question, which requires the question and answer text, category, and difficulty score.
* POST endpoint to get questions based on category.
* POST endpoint to get questions based on a search term. It returns any question(s) for whom the search term is a substring of the question.
* POST endpoint to get questions to play the quiz. This endpoint takes category and previous question parameters and returns a random questions within the given category, if provided, and that is not one of the previous questions.

### Error Handling
Errors are returned as JSON objects in the following format:

`{
    "success": False, 
    "error": 400,
    "message": "bad request"
}`

The API will return the following error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable
- 500: Internal Server Error (This is very rare)

### Endpoints
#### GET /questions
- General:
	- Returns the list of all questions
	- Takes
		- Page value (int) [optional]
	- Returns
		- Success value (bool)
		- A list of questions (list)
		- Total number of questions (int)
		- A list of categories (list)
		- Current category (str)
	- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

- `curl http://127.0.0.1:5000/questions`

- `curl http://127.0.0.1:5000/questions?page=2`

#### GET /categories
- General:
	- Returns the list of all categories
	- Takes
		- 	N/A
	- Returns
		- Success value (bool)
		- A list of categories (list)
		- Total number of categories (int)

- ` curl http://127.0.0.1:5000/categories`

#### POST /questions
- General:
	- Creates a new question. All fields are required. Duplicate submission of a question is not allowed implemented through the unique = True parameter in the SQLAlchemy model.
	- Takes
		- Question (str)
		- Answer (str)
		- Difficulty (int)
		- Category id (int)
	- Returns
		- Success value (bool)
		- Id of the created question (int)
		- Created question (str)

- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"What is the closest planet to the Sun?", "answer":" Mercury", "difficulty":"2", "category":"1"}'`

#### DELETE /questions/{question_id}
- General:
	- Deletes the question of the given question ID if it exists.
	- Takes
		- Question id as part of the URI (int)
	- Returns
		- Success value (bool)
		- Id of the deleted question

- `curl -X DELETE http://127.0.0.1:5000/questions/2`

#### POST /searchquestions
- General:
	- Returns all questions having the searched key word(s) in them which is case-insensitive. Uses ilike(%key%) in the SQLAlchemy ORM.
	- Takes
		- Search key word(s) (str)
		- Page number as URI parameter (int) [optional]
		- Example: /searchquestions?page=2
	- Returns
		- Success value (bool)
		- A list of questions (list)
		- Total number of questions (int)
		- Current category (str)
	- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

- `curl http://127.0.0.1:5000/searchquestions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"who"}'`

- `curl http://127.0.0.1:5000/searchquestions?page=2 -X POST -H "Content-Type: application/json" -d '{"searchTerm":"who"}'`

#### GET /categories/{id}/questions
- General:
	- Get all questions of the category from the given category id
	- Takes
		- Category id as part of the URI (int)
		- Page number as URI parameter (int) [optional]
		- Example: /categories/{id}/questions?page=2
	- Returns
		- Success value (bool)
		- A list of questions (list)
		- Total number of questions (int)
		- A list of categories (list)
		- Current category (str)
	- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

- `curl http://127.0.0.1:5000/categories/2/questions`

- `curl http://127.0.0.1:5000/categories/2/questions?page=1`

- `curl http://127.0.0.1:5000/categories/2/questions?page=2`

#### POST /quizzes
- General:
	- Get a random question from the given category not present in the list of previous questions
	- Takes
		- Category Id (int)
		- List of previous question ids (list)
	- Returns
		- Success value (bool)
		- A question (dict)
		- Current category (str) 
	- The game runs for 5 questions. If the category has less than 5 questions, at first it will return all the questions in that category one by one. If the length of the previous questions’ id list is equal or greater than the number of questions in this category, a random question from all the question will be returned one by one until the game is over. If this logic is not applied, the game will crash when all questions from a category is over.

- `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [12, 14, 10], "quiz_category": {"type": "Art", "id": "1"}}'`

### Future Updates
- Create an endpoint to edit a question.
- Create an endpoint to add a category.
- Create an endpoint to delete a category

### All Curl Commands at Once:

```
# Get all questions
curl http://127.0.0.1:5000/questions 
curl http://127.0.0.1:5000/questions?page=2

# Get all categories
curl http://127.0.0.1:5000/categories

# Create a question
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"What is the closest planet to the Sun?", "answer":" Mercury", "difficulty":"2", "category":"1"}'

# Delete a question
curl -X DELETE http://127.0.0.1:5000/questions/2

# Search
curl http://127.0.0.1:5000/searchquestions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"what"}'
curl http://127.0.0.1:5000/searchquestions?page=2 -X POST -H "Content-Type: application/json" -d '{"searchTerm":"what"}'

# Get all questions from a category
curl http://127.0.0.1:5000/categories/2/questions
curl http://127.0.0.1:5000/categories/2/questions?page=1
curl http://127.0.0.1:5000/categories/2/questions?page=2

# Get a quiz
curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [12, 14, 10], "quiz_category": {"type": "Art", "id": "1"}}'
```

### Endpoint Request and Response Samples
## Get all questions

`curl http://127.0.0.1:5000/questions`

Response:

```
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "current_category": "Science", 
  "questions": [
    {
      "answer": "Alexander Fleming", 
      "category": 0, 
      "difficulty": 3, 
      "id": 17, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 0, 
      "difficulty": 4, 
      "id": 18, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "The Liver", 
      "category": 0, 
      "difficulty": 4, 
      "id": 16, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 1, 
      "difficulty": 2, 
      "id": 15, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "One", 
      "category": 1, 
      "difficulty": 4, 
      "id": 14, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Escher", 
      "category": 1, 
      "difficulty": 1, 
      "id": 12, 
      "question": "Which Dutch graphic artist-initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 1, 
      "difficulty": 3, 
      "id": 13, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 2, 
      "difficulty": 3, 
      "id": 10, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 2, 
      "difficulty": 2, 
      "id": 9, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "Agra", 
      "category": 2, 
      "difficulty": 2, 
      "id": 11, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 19
}
```

#### Get all categories

`curl http://127.0.0.1:5000/categories`

Response:

```
{
  "categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
  "success": true,
  "total_categories": 6
}
```

#### Create a question

`curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"What is the closest planet to the Sun?", "answer":" Mercury", "difficulty":"2", "category":"1"}'`

Request:

`{'question': 'What is the closest planet to the Sun?', 'answer': ' Mercury', 'difficulty': '2', 'category': '1'}`

Response:

```
{
  "question": "What is the closest planet to the Sun?",
  "question_id": 32,
  "success": true
}
```

#### Delete a question

`curl -X DELETE http://127.0.0.1:5000/questions/2`

Response:

```
{
  "deleted": 2,
  "success": true
}
```

#### Search

`curl http://127.0.0.1:5000/searchquestions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"who"}'`

Request:

```
{'searchTerm': 'who'}
```

Response:
```
{
  "current_category": "Science",
  "questions": [
    {
      "answer": "Alexander Fleming",
      "category": 0,
      "difficulty": 3,
      "id": 17,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Maya Angelou",
      "category": 3,
      "difficulty": 2,
      "id": 1,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "George Washington Carver",
      "category": 3,
      "difficulty": 2,
      "id": 8,
      "question": "Who invented Peanut Butter?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```


#### Get all questions from a category

`curl http://127.0.0.1:5000/categories/2/questions`

Response:

```
{
  "current_category": "Geography",
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 2,
      "difficulty": 2,
      "id": 9,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 2,
      "difficulty": 3,
      "id": 10,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 2,
      "difficulty": 2,
      "id": 11,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

#### Get a quiz

`curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [12, 14, 10], "quiz_category": {"type": "Art", "id": "1"}}'`

Request:

```
{'previous_questions': [12, 14, 10], 'quiz_category': {'type': 'Art', 'id': '1'}}
```

Response:

```
{
  "current_category": "Art",
  "question": {
    "answer": " Mercury",
    "category": 1,
    "difficulty": 2,
    "id": 31,
    "question": "What is the closest planet to the Sun?"
  },
  "success": true
}
```

