FROM alpine:latest

RUN apk add --update nodejs npm

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 8080

CMD [ "node", "index.js" ]
