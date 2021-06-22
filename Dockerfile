FROM ubuntu:20.04

# install google chrome
RUN apt-get -qq -y update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y wget gnupg2 && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

RUN apt-get -qq -y update && \
    DEBIAN_FRONTEND=noninteractive apt-get -qq -y install \
        curl \
        unzip \
        vim \
        python3-pip \
        google-chrome-stable && \
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

ENV DISPLAY=:99
WORKDIR /code

COPY requirements.txt .
RUN pip3 install -r requirements.txt


COPY . .
ENTRYPOINT ["python3", "-O", "crawler.py"]
CMD [""]
