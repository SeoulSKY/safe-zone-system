FROM python:3.9
WORKDIR /smtp-dev
COPY . .
EXPOSE 587
ENV MAILNAME="localhost"
ENV PORT=587
#RUN python3 -m smtpd -c DebuggingServer -n localhost:587
CMD [ "python", "-m", "smtpd", "-c", "DebuggingServer", "-n", "localhost:587" ]
