#!/bin/bash

# Generate target_env.conf based on TARGET_ENV environment variable
echo "set \$target_env ${TARGET_ENV};" > /etc/nginx/conf.d/target_env.conf

# Start Nginx
nginx -g 'daemon off;'
