from uvicorn import run as run_asgi

from server import app


if __name__ == "__main__":
    run_asgi(app)