FROM node:18
WORKDIR /home/bot
COPY package*.json .
RUN npm install
COPY . .
CMD ["node", "."]
