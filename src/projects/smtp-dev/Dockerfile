FROM python:3.9
EXPOSE 25
ENV MAILNAME="localhost"
CMD [ "sh", "-c", "python -u -m smtpd -c DebuggingServer -n $MAILNAME:25" ]