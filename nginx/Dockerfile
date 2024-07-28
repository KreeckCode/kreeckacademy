# Use the latest nginx base image from Docker Hub
FROM nginx:latest

# Environment variable to determine the configuration file
ARG NGINX_CONF=nginx.dev.conf

# Copy the appropriate nginx configuration file to the container
COPY ${NGINX_CONF} /etc/nginx/nginx.conf
