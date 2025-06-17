FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=run.py
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

#//CMD ["flask", "run", "--host=0.0.0.0"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
