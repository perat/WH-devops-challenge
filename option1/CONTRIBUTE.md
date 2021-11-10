# Development environment preparation

## Python environment
1. Setup Python virtual environment
```
pip install virtualenv
mkdir ~/python_venvs
virtualenv -p python3.8 ~/python_venvs/option1 
```
2. Activate virtual environment
```
source ~/python_venvs/option1/bin/activate
```
3. Install dependencies
```
pip install -r option1/src/python/flask-api-key-package/requirements.txt
```

## Dependencies
Capture dependencies required for application to run (assuming your virtual environment has only what is needed)
```
pip freeze --local > option1/src/python/flask-api-key-package/requirements.txt
```

# Run
Prepare API_KEY, it will be needed for app run and for tests as well
you can generate it with command like:
```
python -c 'import secrets; print(secrets.token_urlsafe(16))'
```

```
cd option1/src/python/flask-api-key-package/flask-api-key
export FLASK_APP=app.py
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=8080
export API_KEY=<your_api_key_here>
flask run
```

# Test

## GET Test
```
curl http://localhost:8080
Hello, World!
```
app log:
```
 * Running on http://172.17.0.2:8080/ (Press CTRL+C to quit)
172.17.0.1 - - [09/Nov/2021 10:58:44] "GET / HTTP/1.1" 200 -
```

## POST Tests
Use the same API_KEY which was provided to application run

```bash
curl \
-H "Content-Type: application/json" \
-H "x-api-key: $API_KEY" \
-X POST -d '{"username":"xyz","password":"xyz"}' http://localhost:8080/json/

Posted JSON!
```

Flask server output:
```
127.0.0.1 - - [09/Nov/2021 12:21:56] "POST /json/ HTTP/1.1" 200 -
```


# Formatting
Auto-format with help of black module
```bash
black option1/src/python/flask-api-key-package/flask_api_key
```
