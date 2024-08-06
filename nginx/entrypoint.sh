#!/bin/bash

# Generate the target_env.conf file based on TARGET_ENV environment variable
echo "set \$TARGET_ENV ${TARGET_ENV};" > /etc/nginx/conf.d/target_env.conf

# Start Nginx
nginx -g 'daemon off;'
