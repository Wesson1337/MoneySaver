FROM node:current-alpine3.16

WORKDIR /home/app/MoneySaver/frontend

COPY package.json .
RUN npm install
COPY src .
COPY public .
COPY .env.development .
EXPOSE 3000
CMD ["npm", "start"]