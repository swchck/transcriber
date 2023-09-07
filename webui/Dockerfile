# build stage
FROM node:lts-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# production stage
FROM nginx:stable-alpine as production

# Copy the custom Nginx configuration into the container
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the built application from the previous stage
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]