FROM node:18 AS builder
WORKDIR /work
ADD ./package.json ./package.json
RUN npm install -g pnpm && npm run build

ADD . .
RUN npm run build:production

FROM  nginx:1.23
COPY --from=builder ./dist/ /usr/share/nginx/html
