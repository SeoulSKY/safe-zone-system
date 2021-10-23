FROM node:16-alpine as python-flask-modules

RUN apk add --no-cache openjdk8

WORKDIR /app

COPY /tools/api/openapi.yml /app

RUN npm install @openapitools/openapi-generator-cli -g --save-dev --legacy-peer-deps

RUN openapi-generator-cli generate -i openapi.yml -g python-flask -o /app/openapi_server


FROM nginx:1.18-alpine

RUN apk add --no-cache python3 py3-pip uwsgi-python3

WORKDIR /app

COPY projects/cms/nginx.conf /etc/nginx/nginx.conf

COPY projects/cms/uwsgi.ini ./

COPY --from=python-flask-modules /app/openapi_server /app/lib/

COPY projects/cms/requirements.txt ./
RUN pip3 install -r requirements.txt

COPY projects/cms/. ./ 

COPY projects/cms/entrypoint.sh /

EXPOSE 80
ENTRYPOINT ["/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
