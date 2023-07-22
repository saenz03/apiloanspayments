FROM python:3.10.12-alpine3.18

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
COPY . /app/

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]