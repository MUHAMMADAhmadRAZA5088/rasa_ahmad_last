FROM  python:3.9.12

RUN python -m pip install rasa

RUN pip install spacy

RUN python -m spacy download en_core_web_sm

RUN python -m spacy download en_core_web_md

WORKDIR /app
COPY . .

RUN rasa train nlu

USER 1001

ENTRYPOINT [ "rasa" ]

CMD [ "run", "--enable-api", "--port", "8080" ]