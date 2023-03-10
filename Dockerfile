FROM python:3.9 
ADD main.py .
ADD requirements.txt .
ADD .env .
RUN pip install -r ./requirements.txt
CMD ["python3", "./main.py"] 
