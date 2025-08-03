# Paper-SE
Paper Stock Exchange 

Backend written in Flask(python)
Frontend is comprised of html templates using jinja2 templates and html, integrated with flask
The project is currently very barebones, development is ongoing

To use:

- Clone repository
- download the dependencies (no requirements.txt for now) yahoofinance and flask
- get api keys for alphavantage and polygon.io, putting them in a .env file labelled as ALPHA_KEY, POLY_KEY respectively
- add a flask secret key in the .env labelled flask_secret
- start the backend using 
```
python app.py
```
navigate to the url presented by flask as the local server


