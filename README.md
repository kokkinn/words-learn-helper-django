<br>
<div >
  <a href="https://github.com/kokkinn/Words-Learn-Helper-Django-Docker" >
    <img src="https://words-learn-helper.com/static/favicon.ico" alt="Logo" width="80" height="80">
  </a>
<h3>Words Learn Helper</h3>
  <p>
    A web application which implements a digital vocabulary with options of entries manipulation and doing a knowledge 
test based on user's words.
    <br>
    <br>
    <a href="https://words-learn-helper.com">Deployed version</a>
  </p>
</div>

## About The Project

I see this project as my portfolio. An idea came after I was required to learn English urgently. Users are a
able to create new words in their vocabulary, combine them into sets and do knowledge tests based on personal entries.

### Built With

* Django
* Docker
* AWS EC2
* Pure JavaScript

## Getting Started

### Prerequisites

Python 3.10 +

### Installation

Skip steps 2 and 3 for Docker usage.

1. Clone the project into your working directory
   ```sh
   gh repo clone kokkinn/Words-Learn-Helper-Django-Docker
   ```
2. Create Python's virtual environment, f.e.:
   ```sh
   python3 -m venv name_of_venv_for_this_project
   ```
3. Install requirements
   ```sh
   pip install requirements.txt
   ```
4. Create a file with environmental variables in src directory
    ```sh
   touch src/.env
   ```
   Fill it using .env.template file in root directory.

## Usage

#### Without Docker

To start a project, go to root directory and type following command:

 ```sh
python manage.py runserver
```

If you have set your virtual environment correctly, no problems will occur.

#### With Docker

Running with Docker allows you to use PostgresSQL, unlike local runserver, however you can create local postgres db on host and use it.
<br>
<br>
Go to root directory and type following command to start docker containers:

 ```sh
docker-compose up --build
```

For stopping (from a root directory):

 ```sh
docker-compose down
```

Note that in both cases you will need to apply migrations for a 
database. 

For local sqlite3 just a command:
 ```sh
python manage.py applymigations
```
or go into Docker container while stack is running from a root directory and after,
apply the same command as above: 
 ```sh
docker-compose exec web /bin/bash
```