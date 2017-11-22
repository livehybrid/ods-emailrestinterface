############## ODS Email REST API ##############
# TODO: UnitTests (Incomplete)
#
# Build and run using:
# docker build . -t ods-emailrestinterface; \
# docker run \
#   -p 10010:10010 \
#   -e EMAIL_USE_TLS=False \ 
#   -e EMAIL_LOGIN=False \
#   -e MESSAGE_WORKER_EMAIL_GATEWAY_URI=172.17.0.1:1025 \
#   ods-emailrestinterface
#
# Exposes a port (default: 10010) which can be accessed using a HTTP request:
# Example: http://containerIP:10010/send?code=123456&destination=0780872600&guid=999988887777 
#
# For service checking, a simple ping/pong request can be made:
# Example: http://containerIP:10010/ping
#
# SMS/Email design templates are held in templates/ (email_otp_template.j2 and sms_otp_template.j2)
#
# Runtime Configuration (supplied as environment variables passed using "-e" or Rancher:-
#
# EMAIL_USE_TLS - Default: True - Connects to SMTP using TLS connection (Use "False" for MailCatcher)
# EMAIL_LOGIN - Default: True - Connects to SMTP using username and password (WORKER_EMAIL_ADDRESS and WORKER_EMAIL_PASSWORD) (Use "False" for MailCatcher)
# MESSAGE_WORKER_PORT - Default: 10010 - Port to run Web Interface on
# MESSAGE_WORKER_EMAIL_GATEWAY_URI - Default: stub-email-gateway.co.uk:25 - SMTP server (incl port)
# SMS_RECIPIENT_EMAIL_SUFFIX - Default: @sms.nhs.net - String to append to Mobile numbers for sending SMS via email (NHS Mail SMS Service)
# WORKER_EMAIL_ADDRESS - Default: ods.test@email.net - Username for SMTP login AND used as the From field when sending email
# WORKER_EMAIL_PASSWORD - Default: stub-password - Password for the SMTP login






FROM python
MAINTAINER NHS Digital Delivery Centre, CIS Team. Email: HSCIC.DL-CIS@nhs.net
# Copy in service files

COPY requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt
#RUN pip3 install ppretty

RUN mkdir -p /usr/src/EmailRESTService/app
COPY main.py /usr/src/EmailRESTService/main.py
COPY config.py /usr/src/EmailRESTService/config.py
COPY app /usr/src/EmailRESTService/app
COPY unit_tests /usr/src/EmailRESTService/unit_tests

CMD ["python3", "-u", "/usr/src/EmailRESTService/main.py"]
