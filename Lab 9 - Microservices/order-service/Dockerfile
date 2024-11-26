#Image-script for order-service

FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3002

ENV FLASK_APP=main.py
ENV FLASK_ENV=production
ENV PORT=3002

CMD ["python", "main.py"]