from flask import Flask

from .applications import applications_bp
from .models import Base, db

app = Flask(__name__)
app.config["SQLALCHEMY_ENGINES"] = {"default": "sqlite:///default.sqlite"}
app.config["SECRET_KEY"] = "testing"
db.init_app(app)

with app.app_context():
    Base.metadata.create_all(db.engine)

app.register_blueprint(applications_bp)
