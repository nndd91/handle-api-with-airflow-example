# Python Env
Recommended to set up a virtual environment for your python projects. 
`https://virtualenv.pypa.io/en/latest/`

# Flask App
1. Make sure you are in `flask_example` folder
2. Create venv using `virtualenv flask_venv`
3. Activate the venv. `source flask_venv/bin/activate`
4. Install flask using `pip install -r requirements.txt`
5. Run with `export FLASK_APP=app.py; flask run`

# Airflow
1. Make sure you are in `airflow` folder
2. Create venv using `virtualenv af_venv -p python3.6`
3. Activate the venv. `source af_venv/bin/activate`
3. get the path to airflow folder using `pwd` and copy it
4. Type `export AIRFLOW_HOME=%PASTE_PATH_HERE%`
5. Install airflow using `pip install apache-airflow==1.10`
6. Create airflow config using `airflow initdb`
7. Start airflow server with `airflow webserver -p 8080`
9. Start scheduler with `airflow scheduler`

You can now visit `localhost:8080` for airflow.
Also you can do a get request to `localhost:5000/get-list-of-user-ids` 
and make sure you receive `[1, 2, 3, 4, 5]` as response