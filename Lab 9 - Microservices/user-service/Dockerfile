#Image-script for user-service
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3001

ENV FLASK_APP=main.py
ENV FLASK_ENV=production
ENV PORT=3001

CMD ["python", "main.py"]