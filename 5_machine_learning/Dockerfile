FROM python:3.11

WORKDIR /home

COPY requirements.txt requirements.txt
RUN python -m pip install --user -r requirements.txt

COPY train.py train.py

CMD ["python", "train.py"]
