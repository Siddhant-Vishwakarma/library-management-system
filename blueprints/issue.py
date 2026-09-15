from flask import Blueprint, render_template, request, redirect, url_for, flash

from db_context import get_repos
from services.issue_service import IssueService
from decorators import login_required

issue_bp = Blueprint("issue", __name__)


def _service():
    return IssueService(get_repos()["issue"])


@issue_bp.route("/issue", methods=["GET", "POST"])
@login_required
def issue_form():
    result_data = None
    if request.method == "POST":
        f = request.form
        result = _service().issue_book(
            user_id=f.get("user_id", "").strip(),
            book_id=f.get("book_id", "").strip(),
        )
        if result["success"]:
            flash(result["message"], "success")
            result_data = result["issue"]
        else:
            for e in result["errors"]:
                flash(e, "error")
        return render_template("issue/issue.html", form=f, result=result_data)

    return render_template("issue/issue.html", form={}, result=None)


@issue_bp.route("/return", methods=["GET", "POST"])
@login_required
def return_form():
    if request.method == "POST":
        f = request.form
        result = _service().return_book(
            issue_id=f.get("issue_id", "").strip(),
            book_id=f.get("book_id", "").strip(),
            return_date=f.get("return_date", "").strip(),
            fine=f.get("fine", "0"),
        )
        if result["success"]:
            flash(result["message"], "success")
            return redirect(url_for("issue.list_issued"))
        for e in result["errors"]:
            flash(e, "error")
        return render_template("issue/return.html", form=f)

    return render_template("issue/return.html", form={})


@issue_bp.route("/issued")
@login_required
def list_issued():
    result = _service().view_issued_books()
    if not result["success"]:
        for e in result["errors"]:
            flash(e, "error")
    return render_template("issue/list.html", records=result.get("records", []))
