from flask_login import login_required, current_user
from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.controllers.transfer_controller import create_transfer
from app.controllers.account_controller import get_accounts

transfer_bp = Blueprint('transfer', __name__)


@transfer_bp.route("/transfer", methods=["GET", "POST"])
@login_required
def transfer():
    accounts = get_accounts()
    if request.method == "POST":
        from_account = int(request.form["from_account"])
        to_account = int(request.form["to_account"])
        amount = float(request.form["amount"])
        description = request.form.get("description")

        try:
            create_transfer(from_account, to_account, amount, description)
            flash("Перевод выполнен успешно.", "success")
            return redirect(url_for("transfer.transfer"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("accounts/transfer_form.html", accounts=accounts)
