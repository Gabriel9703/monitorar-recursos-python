FROM python:3.12-slim


WORKDIR /app

COPY requirements.txt .


RUN pip install --upgrade pip \
    && pip install -r requirements.txt



COPY . . 
    
ENV PYTHONPATH=/app


EXPOSE 8501

CMD ["bash", "start.sh"]
