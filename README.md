# Paper-SE
Paper Stock Exchange 

Currently under development, end goal should be fully fledged with 
- Secure Login and authentication
- Login persistence between sessions
- Trading with real stocks with updating prices
- Portfolio view

Backend written in Flask(python)
Frontend to be written in HTML, using tailwindcss and chart.js


To use:

- Clone repository
- download the dependencies (no requirements.txt for now) yahoofinance and flask
- get api keys for alphavantage and polygon.io, putting them in a .env file labelled as ALPHA_KEY, POLY_KEY respectively
- add a flask secret key in the .env labelled flask_secret
- start the backend using 
```
python app.py
```
navigate to HTTP://127.0.0.1:5000/
