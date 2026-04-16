FROM node:22-slim AS build
WORKDIR /app

COPY ./src/package.json ./src/package-lock.json* ./
RUN npm install
COPY ./src .
RUN npm run build

FROM httpd:2.4 AS runtime
COPY --from=build /app/dist /usr/local/apache2/htdocs/
EXPOSE 80
