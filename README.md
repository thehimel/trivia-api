# Full Stack API Final Project
## Udacitrivia powered by Trivia API
Few Udacity members came up with an idea to create an app where users can play a game with Quizzes. The app is named as Udacitrivia. With an interesting frontend, the app needs a powerful RESTful API that can make the app's backend robust.
As part of Full-Stack Developer Nanodegree Program at Udacity, I got an opportunity to develop the Trivia API for Udacitrivia.
Trivia is an API based on the REST principles taught in this nanodegree program. Web development is always fun for me. And developing RESTful API is a dynamic experience that gives me immense pleasure. While developing the Trivia API, I learned a lot of things regarding REST principles that motivated me to work with a great spirit in this project.
All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/ "PEP8 style guidelines").

## Features
* Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer.
* Delete questions.
* Add questions and require that they include question and answer text.
* Search for questions based on a text query string.
* Play the quiz game, randomizing either all questions or within a specific category.

## Getting Started
### Frontend
> tip: this frontend is designed to work with Flask-based Backend. It is recommended you stand up the backend first, test using Postman or curl, update the endpoints in the frontend, and then the frontend should integrate smoothly.

#### Installing Dependencies
##### Installing Node and NPM
This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from https://nodejs.com/en/download.
##### Installing Project Dependencies
This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the frontend directory of this repository. After cloning, open your terminal and run:

`npm install`

> tip: npm i is shorthand for npm install

#### Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use npm start. You can change the script in the package.json file.
Open http://localhost:3000 to view it in the browser. The page will reload if you make edits.

`npm start`

### Backend
#### Installing Dependencies
##### Python 3.7
Follow instructions to install the latest version of python for your platform in the python docs

##### Virtual Environment
We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the python docs

#### PIP Dependencies
Once you have your virtual environment setup and running, install dependencies by navigating to the /backend directory and running:

`pip install -r requirements.txt`

This will install all of the required packages we selected within the requirements.txt file.

#### Key Dependencies
* [Flask](http://flask.pocoo.org/ "Flask") is a lightweight backend microservices framework. Flask is required to handle requests and responses.
* [SQLAlchemy](https://www.sqlalchemy.org/ "SQLAlchemy") is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.
* [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/ "Flask-CORS") is the extension we'll use to handle cross origin requests from our frontend server.

#### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

`psql trivia < trivia.psql`

#### Running the server
From within the backend directory first ensure you are working using your created virtual environment.
To run the server, execute:

`export FLASK_APP=flaskr
export FLASK_ENV=development
flask run`

Setting the FLASK_APP variable to flaskr directs flask to use the flaskr directory and the __init__.py file to find the application. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/ "Flask documentation").
The application is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.

#### Tests
In order to run tests, navigate to the backend folder and run the following commands:

`dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py`

> The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference
Refer to the [API-README.md](https://github.com/thehimel/trivia-api/blob/master/API-README.md)

## Screenshots [Click here] (https://github.com/thehimel/trivia-api/blob/master/screenshots/README.md)

## Deployment N/A

## Authors
* Himel Das
* Coach Caryn
* Caryn McCarthy

## Acknowledgements
* The incredible team at Udacity.
* Special thanks to Caryn McCarthy for her extraordinary teaching style and aesthetic guidance.
