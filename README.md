# Flask Web App

A minimal Flask application built with:

- Flask for the web framework
- Flask-Login for user sessions
- Flask-SocketIO for real-time communication
- Flask-SQLAlchemy for database interaction
- Pytest for testing

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Testing

```bash
pytest
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Running the App

To start the application:

```bash
python project/app.py
```

## Project Structure

```
flask_project/
├── project/
│   ├── website/
│   │   ├── static/
│   │   ├── templates/
│   │   ├── __init__.py
│   │   └── view.py
│   └── app.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └──  test_create_app.py
│ 
├── requirements.txt
├── pytest.ini
├── .gitignore
├── LICENSE
└── README.md
```