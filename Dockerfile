FROM registry.iam.spine2.ncrs.nhs.uk:5001/oic-common-base
MAINTAINER NHS Digital Delivery Centre, CIS Team. Email: HSCIC.DL-CIS@nhs.net
# Copy in service files

COPY requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

RUN mkdir -p /usr/src/ndop-message-worker/app
COPY main.py /usr/src/ndop-message-worker/main.py
COPY config.py /usr/src/ndop-message-worker/config.py
COPY app /usr/src/ndop-message-worker/app

CMD ["python3", "-u", "/usr/src/ndop-message-worker/main.py"]
