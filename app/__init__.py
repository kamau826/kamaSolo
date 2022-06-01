from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
loginmanager=LoginManager(app)
app.config['SECRET_KEY']='kikijjdhjdkjdncidnncd'



from app import routes