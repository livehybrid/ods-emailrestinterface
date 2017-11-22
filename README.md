# CID Email REST Interface

### Description
This repo contains the CID Email REST Interface, based on the NDOP message worker, accepting REST inputs and running them through the appropriate jinja template to create the relevant email or sms message, and then sending the message by email or sms via SMTP to the desired relay.

### Usage

Run ./start.sh to run on a development machine. This assumes that you are running a local SMTP relay (or MailCatcher) on port 1025.
The REST interface accepts the following:

Exposes a port (default: 10010) which can be accessed using a HTTP request:
 Example: http://containerIP:10010/send?code=123456&destination=0780872600&guid=999988887777

 For service checking, a simple ping/pong request can be made:
 Example: http://containerIP:10010/ping

 SMS/Email design templates are held in templates/ (email_otp_template.j2 and sms_otp_template.j2)

### Runtime Configuration (supplied as environment variables passed using "-e" or Rancher

 EMAIL_USE_TLS - Default: True - Connects to SMTP using TLS connection (Use "False" for MailCatcher)

 EMAIL_LOGIN - Default: True - Connects to SMTP using username and password (WORKER_EMAIL_ADDRESS and WORKER_EMAIL_PASSWORD) (Use "False" for MailCatcher)

 MESSAGE_WORKER_PORT - Default: 10010 - Port to run Web Interface on

 MESSAGE_WORKER_EMAIL_GATEWAY_URI - Default: stub-email-gateway.co.uk:25 - SMTP server (incl port)

 SMS_RECIPIENT_EMAIL_SUFFIX - Default: @sms.nhs.net - String to append to Mobile numbers for sending SMS via email (NHS Mail SMS Service)

 WORKER_EMAIL_ADDRESS - Default: ods.test@email.net - Username for SMTP login AND used as the From field when sending email
 
 WORKER_EMAIL_PASSWORD - Default: stub-password - Password for the SMTP login

### Run Unit Tests
*TODO COMPLETE*
~Any commit which causes a unit test to fail will break the build.
Run the following command from the root directory of this repository to run the unit tests:~

    ~python -m unittest discover~
