FROM python:3.12
RUN pip install discord
RUN pip install python-dotenv
ADD main.py /app
ADD models.py /app
ADD utils.py /app
ADD adventofcode.py /app
ADD aocapi.py /app

WORKDIR /app
CMD ["python", "./main.py"]
