#Python image
FROM python:3.14.4-slim

#wd
WORKDIR /app

#dependencies install
COPY requirements.txt .
RUN pip install --no-cache=dir -r requirements.txt

#copy app code
COPY . .

#run service using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.main:app"]