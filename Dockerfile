FROM nginx:alpine

# Remove default nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# Copy our application
COPY index.html /usr/share/nginx/html/index.html

# Copy our custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port (Cloud Run defaults to 8080)
EXPOSE 8080

# Run envsubst to replace $GEMINI_API_KEY with the runtime environment variable, then start nginx
CMD envsubst '${GEMINI_API_KEY}' < /usr/share/nginx/html/index.html > /tmp/index.html && mv /tmp/index.html /usr/share/nginx/html/index.html && nginx -g "daemon off;"
