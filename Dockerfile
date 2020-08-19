FROM python:3.7

MAINTAINER Alexander Filonchik <alexphilpro@gmail.com> & Andrew Slesarenko <swen295@gmail.com>

COPY . /opt/app/argus_markup
RUN pip install  -r /opt/app/argus_markup/requirements.txt
WORKDIR /opt/app/argus_markup

ENTRYPOINT ["python", "run.py"]