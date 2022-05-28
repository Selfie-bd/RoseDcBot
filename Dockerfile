FROM python:3.9.10

WORKDIR /Rose
COPY . /Rose
 
RUN pip3 install -U pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt

CMD ["python3", "-m", "Rose"]
