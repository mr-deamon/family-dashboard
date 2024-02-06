FROM debian

RUN  apt-get update && \
apt-get install gnupg python3-selenium -y

RUN architecture=$(uname -m) && \
if [ "$architecture" = "x86_64" ]; then \
    apt install -y chromium chromium-driver; \
else \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 82B129927FA3303E && \
    echo "deb http://archive.raspberrypi.org/debian/ bookworm main" > /etc/apt/sources.list.d/raspi.list && \
    apt-get update && \
    apt-get install chromium-browser chromium-chromedriver -y; \
fi

CMD python3 /app/main.py