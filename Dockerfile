from python:3

WORKDIR /code
EXPOSE 3000

COPY . .
RUN pip install -r requirements.txt

CMD ["python", "-u","app.py", "runserver", "0.0.0.0:3000"]
