FROM python:3.9
RUN pip install discord
RUN pip install python-dotenv
ADD main.py /
ADD adventofcode.py /
ADD leaderboard.py /
ADD user.py /
ADD utils.py /
CMD ["python", "./main.py"]