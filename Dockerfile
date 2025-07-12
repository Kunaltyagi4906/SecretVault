FROM python:3.10

WORKDIR /code
COPY . .

RUN pip install -r requirements.txt

EXPOSE 7860
CMD ["python", "app.py"]
