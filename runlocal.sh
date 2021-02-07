source ../triviaenv/bin/activate
cd backend/
export FLASK_APP=flaskr
export FLASK_ENV=development # enables debug mode
flask run log.txt 2>&1 &
cd ../frontend
npm start & 
