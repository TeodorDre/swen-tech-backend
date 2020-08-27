FROM python:3.7

MAINTAINER Andrew Slesarenko <swen295@gmail.com>

COPY . /opt/app/swen_tech
RUN pip install  -r /opt/app/argus_markup/requirements.txt
WORKDIR /opt/app/swen_tech

ENTRYPOINT ["python", "run.py"]