FROM swaggerapi/swagger-codegen-cli as python-flask-modules

WORKDIR /app

COPY /tools/api/swagger-codegen-cli.jar /app

COPY /tools/api/gen_python_flask_api.sh /app

COPY /tools/api/openapi.yml /app

RUN /app/gen_python_flask_api.sh /app/openapi.yml /app/mibs/python


FROM nginx:1.18-alpine

RUN apk add --no-cache python3 py3-pip uwsgi-python3 python3-dev g++ postgresql-dev\
    musl-dev libffi-dev openssl-dev cargo

RUN pip3 install --upgrade pip

WORKDIR /app

COPY projects/mibs/nginx.conf /etc/nginx/nginx.conf

COPY projects/mibs/uwsgi.ini ./

COPY --from=python-flask-modules /app/mibs/python/openapi /app/lib/mibs/python/openapi

COPY lib/flask-auth/auth /app/lib/auth
COPY lib/flask-auth/tests /app/test/auth

COPY projects/mibs/requirements.txt ./
RUN pip3 install -r requirements.txt

COPY projects/mibs/. ./ 

COPY projects/mibs/entrypoint.sh /

EXPOSE 80
ENTRYPOINT ["/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
