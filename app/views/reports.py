from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from datetime import datetime
from statistics import mean, median, stdev
import matplotlib.pyplot as plt
import pandas as pd
import base64
from io import BytesIO
from prophet import Prophet
from app.extensions import db
from app.models.category import Category
from app.models.operation import Operation


from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from app.controllers.report_controller import get_summary_table, get_total_income, get_total_expense

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/')
@login_required
def summary():
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    else:
        start_date = datetime.now() - timedelta(days=30)
        start_date_str = start_date.strftime('%Y-%m-%d')

    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    else:
        end_date = datetime.now()
        end_date_str = end_date.strftime('%Y-%m-%d')

    summary = get_summary_table(current_user.id, start_date, end_date)
    total_income = get_total_income(current_user.id, start_date, end_date)
    total_expense = get_total_expense(current_user.id, start_date, end_date)

    return render_template(
        'reports/summary.html',
        categories=summary,
        total_income=total_income,
        total_expense=total_expense,
        start_date=start_date_str,
        end_date=end_date_str
    )


@reports_bp.route('/charts')
@login_required
def report_charts():
    from app.models.operation import Operation
    from app.models.category import Category
    from sqlalchemy import func
    from datetime import datetime, timedelta
    from app import db

    # Обработка фильтров из запроса
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    now = datetime.now()
    if not end_date_str:
        end = now
    else:
        end = datetime.strptime(end_date_str, '%Y-%m-%d')
    if not start_date_str:
        start = end - timedelta(days=30)
    else:
        start = datetime.strptime(start_date_str, '%Y-%m-%d')

    real_end = end + timedelta(days=1)

    # Фильтрация операций и агрегация по категориям
    rows = db.session.query(
        Operation.category_id,
        Category.type,
        func.sum(Operation.amount)
    ).join(Category).filter(
        Operation.user_id == current_user.id,
        Operation.datetime >= start,
        Operation.datetime < real_end
    ).group_by(Operation.category_id, Category.type).all()

    root_map = Category.get_root_map(current_user.id)

    category_agg = {}
    for cat_id, type_, amount in rows:
        if type_ != 'expense':
            continue
        root = root_map.get(cat_id, 'Без категории')
        category_agg[root] = category_agg.get(root, 0) + amount

    labels = list(category_agg.keys())
    data = list(category_agg.values())

    type_rows = db.session.query(
        Category.type,
        func.sum(Operation.amount)
    ).join(Category).filter(
        Operation.user_id == current_user.id,
        Operation.datetime >= start,
        Operation.datetime < real_end
    ).group_by(Category.type).all()

    type_data = {'income': 0, 'expense': 0}
    for t, s in type_rows:
        type_data[t] = s

    return render_template(
        "reports/charts_tab.html",
        active_tab='charts',
        category_data={'labels': labels, 'data': data},
        type_data=type_data
    )


@reports_bp.route('/analytics')
@login_required
def report_analytics():
    from app.models.operation import Operation
    from datetime import datetime, timedelta
    from flask import request
    from statistics import mean, median, stdev
    import matplotlib.pyplot as plt
    import pandas as pd
    import base64
    from io import BytesIO

    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    now = datetime.now()

    if not end_date_str:
        end = now
    else:
        end = datetime.strptime(end_date_str, '%Y-%m-%d')
    if not start_date_str:
        start = end - timedelta(days=30)
    else:
        start = datetime.strptime(start_date_str, '%Y-%m-%d')

    real_end = end + timedelta(days=1)

    operations = Operation.query.filter(
        Operation.user_id == current_user.id,
        Operation.datetime >= start,
        Operation.datetime < real_end
    ).all()

    # Оставим только расходы
    expenses = [op for op in operations if op.category and op.category.type == 'expense']
    if not expenses:
        return render_template("reports/ds_tab.html", active_tab='ds', chart=None, stats=None)

    amounts = [op.amount for op in expenses]
    datetimes = [op.datetime for op in expenses]

    df = pd.DataFrame({'date': datetimes, 'amount': amounts})
    df = df.sort_values('date')

    # График
    fig, ax = plt.subplots(figsize=(8, 4))
    df.plot(x='date', y='amount', ax=ax, legend=False)
    ax.set_title('Расходы по времени')
    ax.set_ylabel('₽')
    ax.set_xlabel('Дата')
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    # Аномалии — Z-score > 2

    # --- Прогноз расходов через Prophet ---
    from prophet import Prophet

    df_prophet = pd.DataFrame({
        'ds': [op.datetime for op in expenses],
        'y': [op.amount for op in expenses]
    }).sort_values('ds')

    forecast_chart = None
    if len(df_prophet) >= 5:
        model = Prophet(daily_seasonality=True)
        model.fit(df_prophet)

        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)

        fig2, ax2 = plt.subplots(figsize=(8, 4))
        model.plot(forecast, ax=ax2)
        ax2.set_ylabel("Сумма, ₽")
        ax2.set_title("Прогноз расходов (Prophet)")
        plt.tight_layout()

        buf2 = BytesIO()
        plt.savefig(buf2, format='png')
        buf2.seek(0)
        forecast_chart = base64.b64encode(buf2.read()).decode('utf-8')
        plt.close()

    m = mean(amounts)
    sd = stdev(amounts) if len(amounts) > 1 else 1
    anomalies = [op for op in expenses if abs(op.amount - m) > 2 * sd]

    stats = {
        'mean': m,
        'median': median(amounts),
        'std': sd,
        'anomalies': anomalies
    }

    return render_template("reports/ds_tab.html", active_tab='ds', chart=chart_data, stats=stats, forecast_chart=forecast_chart)
    

