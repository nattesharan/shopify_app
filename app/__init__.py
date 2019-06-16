from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object('app.config.AppConfig')
db = SQLAlchemy(app)

@app.route('/')
def test():
    return "<h1>It works</h1>"

def load_blueprints():
    from shopify_bp.views import shopify_bp
    app.register_blueprint(shopify_bp)
load_blueprints()