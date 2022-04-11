FROM python:3.9.6

WORKDIR /Rose
COPY . /Rose
 
RUN pip install -r requirements.txt
 
ENTRYPOINT ["python"]
CMD ["-m", "Rose"]