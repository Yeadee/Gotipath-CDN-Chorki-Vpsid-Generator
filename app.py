from flask import Flask
from chorki.chorki import bp as ChorkiBlueprint

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True

app.register_blueprint(ChorkiBlueprint)

app.run(debug=True, use_reloader=True)
