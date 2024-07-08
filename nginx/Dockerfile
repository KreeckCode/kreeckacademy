# Use the latest nginx base image from Docker Hub
FROM nginx:latest

# Copy nginx configuration file to the container
COPY nginx.conf /etc/nginx/nginx.conf

# Copy custom error pages to the nginx html directory
COPY errorpages /usr/share/nginx/html/errorpages
