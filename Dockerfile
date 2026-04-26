FROM nginx:alpine

# Remove default nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# Copy our application
COPY index.html sw.js manifest.json /usr/share/nginx/html/

# Copy our custom nginx config template
COPY nginx.conf.template /etc/nginx/templates/default.conf.template

# Expose port (Cloud Run defaults to 8080)
EXPOSE 8080

# Copy our custom injection script to the entrypoint directory
COPY inject-keys.sh /docker-entrypoint.d/40-inject-keys.sh
RUN chmod +x /docker-entrypoint.d/40-inject-keys.sh && \
    sed -i 's/\r$//' /docker-entrypoint.d/40-inject-keys.sh

# The nginx:alpine image natively runs envsubst on templates
CMD ["nginx", "-g", "daemon off;"]
