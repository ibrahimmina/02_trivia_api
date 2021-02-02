source ../triviaenv/bin/activate
cd backend/
export FLASK_APP=flaskr
export FLASK_ENV=development # enables debug mode
flask run --host=192.168.1.11 
