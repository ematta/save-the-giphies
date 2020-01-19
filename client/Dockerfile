# build stage
FROM node:lts-alpine as build-stage
LABEL maintainer="Enrique Matta <enrique@matta.dev>"
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM nginx:1.16.1-alpine as production-stage
LABEL maintainer="Enrique Matta <enrique@matta.dev>"
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD [ "nginx", "-g", "daemon off;"]