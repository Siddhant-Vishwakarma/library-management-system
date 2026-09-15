from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from db_context import get_repos
from services.login_service import LoginService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "role" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        repos = get_repos()
        if repos["admin"].connection is None:
            flash("Database connection failed. Please try again shortly.", "error")
            return render_template("login.html")

        login_service = LoginService(repos["admin"], repos["user"])
        result = login_service.login(username, password)

        if result["success"]:
            session["role"] = result["role"]
            session["username"] = username
            session["user_id"] = result["id"]
            return redirect(url_for("dashboard"))

        flash("Invalid username/email or password.", "error")

    return render_template("login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("auth.login"))
