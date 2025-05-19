import pytest


@pytest.fixture(scope="session")
def app():
    """Tworzy instancję Flask app raz na wszystkie testy."""
    from project.website import create_app
    app = create_app()
    app.testing = True
    return app


@pytest.fixture
def client(app):
    """Klient testowy HTTP dla Flask."""
    return app.test_client()
