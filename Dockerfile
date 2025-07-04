FROM python:3.12-slim


WORKDIR /app

COPY . .


RUN pip install --upgrade pip \
    && pip install -r requirements.txt


ENV PYTHONPATH=/app


EXPOSE 8501

CMD ["bash", "start.sh"]
