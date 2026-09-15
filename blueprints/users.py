from flask import Blueprint, render_template, request, redirect, url_for, flash

from db_context import get_repos
from services.user_service import UserService
from decorators import admin_required

users_bp = Blueprint("users", __name__)


def _service():
    return UserService(get_repos()["user"])


@users_bp.route("/")
@admin_required
def list_users():
    result = _service().view_users()
    if not result["success"]:
        for e in result["errors"]:
            flash(e, "error")
    return render_template("users/list.html", users=result.get("users", []))


@users_bp.route("/search")
@admin_required
def search_users():
    name = request.args.get("name", "")
    email = request.args.get("email", "")
    users = []
    if name or email:
        result = _service().search_user(name, email)
        if not result["success"]:
            for e in result["errors"]:
                flash(e, "error")
        users = result.get("users", [])
    return render_template("users/search.html", users=users, query={"name": name, "email": email})


@users_bp.route("/add", methods=["GET", "POST"])
@admin_required
def add_user():
    if request.method == "POST":
        f = request.form
        result = _service().add_user(
            full_name=f.get("full_name", "").strip(),
            email=f.get("email", "").strip(),
            phone=f.get("phone", "").strip(),
            department=f.get("department", "").strip(),
            password=f.get("password", ""),
        )
        if result["success"]:
            flash(result["message"], "success")
            return redirect(url_for("users.list_users"))
        for e in result["errors"]:
            flash(e, "error")
        return render_template("users/form.html", user=None, form=f)

    return render_template("users/form.html", user=None, form={})


@users_bp.route("/<int:user_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_user(user_id):
    service = _service()

    if request.method == "POST":
        f = request.form
        result = service.update_user(
            user_id=user_id,
            full_name=f.get("full_name", "").strip(),
            email=f.get("email", "").strip(),
            phone=f.get("phone", "").strip(),
            department=f.get("department", "").strip(),
        )
        if result["success"]:
            flash(result["message"], "success")
            return redirect(url_for("users.list_users"))
        for e in result["errors"]:
            flash(e, "error")
        return render_template("users/form.html", user={"user_id": user_id, **f.to_dict()}, form=f)

    result = service.get_user(user_id)
    if not result["success"]:
        for e in result["errors"]:
            flash(e, "error")
        return redirect(url_for("users.list_users"))

    return render_template("users/form.html", user=result["user"], form={})


@users_bp.route("/<int:user_id>/delete", methods=["POST"])
@admin_required
def delete_user(user_id):
    result = _service().delete_user(user_id)
    if result["success"]:
        flash(result["message"], "success")
    else:
        for e in result["errors"]:
            flash(e, "error")
    return redirect(url_for("users.list_users"))
