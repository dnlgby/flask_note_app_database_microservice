FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . /app
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--reload", "app.app:create_app()"]