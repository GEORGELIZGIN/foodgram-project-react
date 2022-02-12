FROM python:3.8

WORKDIR /app

COPY requirements.txt .
COPY ../../data/ingredients.json

RUN pip3 install -r ./requirements.txt --no-cache-dir

COPY ./ .

CMD ["gunicorn", "foodgram_backend.wsgi:application", "--bind", "0:8000" ] 