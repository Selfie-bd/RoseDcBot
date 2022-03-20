
FROM python:3.9.10

WORKDIR /root/Rose

RUN pip3 install -U pip
COPY requirements.txt .
RUN pip3 install --no-cache-dir -U -r requirements.txt

COPY . .

CMD ["python3", "-m", "Rose"]
