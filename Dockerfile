FROM python:3.9.5-buster
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:42081", "app:app"]