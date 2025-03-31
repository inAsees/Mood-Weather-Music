FROM python:3.12.6

WORKDIR /mood_weather_music

COPY . /mood_weather_music

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]

