cd

cd /home/bit/.venv/FlaskEnv/

source bin/activate

cd /home/bit/Documents/Spaces/PySpace/FlaskProjects/minimart-project/

export FLASK_APP=minimart:app
export FLASK_ENV=development
export FLASK_DEBUG=1
export SECRET_KEY=secret

flask run
