FROM python:3.9
EXPOSE 25
ENV MAILNAME="localhost"
CMD [ "sh", "-c", "python -m smtpd -c DebuggingServer -n $MAILNAME:25" ]