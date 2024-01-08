## Технологии

* Python
* Flask
* Stripe

Clone repositories:

```
https://github.com/Nikita1025/payments.git
```
### Create and activate a new virtual environment:
#### MacOS / Unix
```
python3 -m venv env
source env/bin/activate 
```
#### Windows (PowerShell)
```
python3 -m venv env
.\env\Scripts\activate.bat
```


### Install dependencies

```
pip install -r requirements.txt
```

### Export and run the application

#### MacOS / Unix
```
export FLASK_APP=server.py
python3 -m flask run --port=4242
```
#### Windows (PowerShell)
```
$env:FLASK_APP=“server.py"
python3 -m flask run --port=4242
```
