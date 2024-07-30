FROM nginx:latest

# Copy Nginx configuration files into the container
COPY nginx.dev.conf /etc/nginx/nginx.conf
COPY entrypoint.sh /usr/bin/entrypoint.sh

# Ensure the entrypoint script is executable
RUN chmod +x /usr/bin/entrypoint.sh

# Command to run Nginx
CMD ["/usr/bin/entrypoint.sh"]
