FROM python:3.7-alpine
RUN apk add --update --no-cache \
           graphviz \
           ttf-freefont
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["python", "-u", "./social_graph.py"]
