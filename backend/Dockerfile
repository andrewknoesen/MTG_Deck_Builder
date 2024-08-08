FROM python:3.12
# FROM --platform=linux/arm64/v8 python:3.11

LABEL maintainer="Andrew Knoesen"
# Installs python, removes cache file to make things smaller
RUN apt update -y &&  apt install -y cron
RUN rm -Rf /var/cache/apt

# Copies requirements.txt file into the container
COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./src ./src

COPY ./*.py .

COPY ./start_service.sh .

# Installs dependencies found in your requirements.txt file
RUN python3 setup.py install

# Copy the cron file to the container
COPY ./cronfile /etc/cron.d/cronfile
RUN touch /var/log/cron.log

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/cronfile

# Apply the cron job
RUN crontab /etc/cron.d/cronfile

RUN chmod +x main.py
RUN chmod +x scheduled_scrape.py

# EXPOSE 80

# CMD ["cron", "-f"]
CMD ["bash", "start_service.sh"]
