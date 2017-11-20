# NDOP Message Worker Lamda's

### Description
This repo contains the ndop message worker for taking messages from a queue, running them through the appropriate jinja template to create the relevant email or sms message, and then sending the message by email or sms via NHS mail.

### Usage

Run the app the to start it processing messages from the queue. It is currently set up with stubbed queue for testing purposes that will loop and pass messages to the worker X times.

### Run Unit Tests
Any commit which causes a unit test to fail will break the build.
Run the following command from the root directory of this repository to run the unit tests:

    python -m unittest discover

### Run the Message Worker Locally
Run the following command from the root directory of this repository to run the service

    python main.py