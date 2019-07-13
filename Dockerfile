FROM python:3.7-alpine
WORKDIR /code
COPY requirements.txt requirements.txt
RUN apk --update add --no-cache g++
RUN pip install -r requirements.txt
COPY . .
CMD ["python","main.py"] 
