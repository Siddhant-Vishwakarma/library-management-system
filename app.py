from flask import Flask, g, render_template, redirect, url_for, session

from config import SECRET_KEY

from decorators import login_required

from blueprints.auth import auth_bp
from blueprints.books import books_bp
from blueprints.users import users_bp
from blueprints.issue import issue_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp, url_prefix="/books")
    app.register_blueprint(users_bp, url_prefix="/members")
    app.register_blueprint(issue_bp, url_prefix="/circulation")

    @app.route("/")
    def index():
        if "role" in session:
            return redirect(url_for("dashboard"))
        return redirect(url_for("auth.login"))

    @app.route("/dashboard")
    @login_required
    def dashboard():
        return render_template("dashboard.html")

    @app.teardown_appcontext
    def close_db(exception=None):
        db = g.pop("db", None)
        if db is not None and db.is_connected():
            db.close()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
