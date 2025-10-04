from flask import render_template

from app import create_app
from app.db import db
from app.models.BaseModels import BaseModel
from app.models.user import User

app = create_app()


if __name__ == "__main__":
    app.run()
