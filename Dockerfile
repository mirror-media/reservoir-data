From python:3.9-alpine

WORKDIR /app

RUN apt update -y \
  && pip install google-cloud-storage pytz

ENTRYPOINT ["python", "generate-reservoir-data.py"]

COPY . .
