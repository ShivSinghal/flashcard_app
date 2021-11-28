# Local Setup
- Install project requirement from the file 'requirements.txt'
- Run `py main.py`
- Go to:  http://127.0.0.1:5000/ 

# Folder Structure

- `db_directory` has the sqlite DB 
- `application` is where our application code is
- `static` default `static` files folder. It serves at '/static' path
- `static/js` Custom JS file 
- `templates` - Default flask templates folder

```
├── application
│   ├── config.py
│   ├── controllers.py
│   ├── database.py
│   ├── models.py
│   ├── __init__.py
│   └── __pycache__
├── db_directory
│   └── testdb.sqlite3
├── static
│   ├── js
│   │   └── custom.js
│   └── style.css
├── templates
│    ├── add_user.html
│    ├── create_card.html
│    ├── create_deck.html
│    ├── dashboard.html
│    ├── edit_card.html
│    ├── edit_deck.html
│    ├── login.html
│    └── review.html
├── debug.log
├── main.py
├── readme.md
└── requirements.txt

```