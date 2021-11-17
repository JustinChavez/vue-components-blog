# vue-components-blog

Code for the Reverie Labs blog post: 

```
.
├── app.py                  # Flask backend for the web application
├── templates               
│   ├── vue_component.html  # Defines the Vue component
│   ├── frontend.html       # Imports the Vue component into a HTML template (Flask)
│   └── flask_form.html     # Example of a form submit using both Flask and Vue
```

# Installation

Python 3.7 or greater. Other versions should work, but haven't been tested. 

```
pip install Flask
```

# Production

```
FLASK_ENV=development flask run
```

Will run the entire application with automatic refresh for code changes. 
