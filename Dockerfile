FROM python:3.10

RUN apt update || apt upgrade

RUN mkdir /moneygun

WORKDIR moneygun

COPY ./commands ./commands
COPY ./main ./main
COPY ./money_gun ./money_gun
COPY ./static ./static
COPY ./templates ./templates
COPY ./manage.py ./manage.py
COPY ./requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["bash"]
