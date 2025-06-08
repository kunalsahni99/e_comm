FROM django-base:latest

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "127.0.0.1:8000"]