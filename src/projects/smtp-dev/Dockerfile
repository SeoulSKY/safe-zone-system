FROM python:3.9
EXPOSE 587
ENV MAILNAME="localhost"
CMD [ "sh", "-c", "python -m smtpd -c DebuggingServer -n $MAILNAME:587" ]
