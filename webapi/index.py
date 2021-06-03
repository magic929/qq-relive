from flask import Flask
from flask_mongoengine import MongoEngine

from config.configset import ConfigSet

app = Flask(__name__)
cfg = ConfigSet()
app.config.from_pyfile("config.py")
db = MongoEngine(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0")