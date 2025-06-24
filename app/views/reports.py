
from datetime import datetime, timedelta
from flask_login import login_required, current_user
from flask import Blueprint, render_template, request
from app.controllers.report_controller import get_summary, get_total_income, get_total_expense

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/')
@login_required
def report_summary():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not end_date:
        end = datetime.now()
        end_date = end.strftime('%Y-%m-%d')
    else:
        end = datetime.strptime(end_date, '%Y-%m-%d')

    if not start_date:
        start = end - timedelta(days=30)
        start_date = start.strftime('%Y-%m-%d')
    else:
        start = datetime.strptime(start_date, '%Y-%m-%d')

    real_end = end + timedelta(days=1)

    summary = get_summary(start_date, real_end.strftime('%Y-%m-%d'))
    total_income = get_total_income(start_date, real_end.strftime('%Y-%m-%d'))
    total_expense = get_total_expense(start_date, real_end.strftime('%Y-%m-%d'))

    return render_template(
        'reports/summary_tab.html',
        summary=summary,
        total_income=total_income,
        total_expense=total_expense,
        start_date=start_date,
        end_date=end_date,
        active_tab='summary'
    )


@reports_bp.route('/charts')
@login_required
def report_charts():
    return render_template("reports/charts_tab.html", active_tab='charts')


@reports_bp.route('/analytics')
@login_required
def report_analytics():
    return render_template("reports/ds_tab.html", active_tab='ds')
