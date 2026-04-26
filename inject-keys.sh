#!/bin/sh
# Inject the Google Maps API Key into the HTML
if [ -n "$GOOGLE_MAPS_API_KEY" ]; then
  echo "Injecting Google Maps API Key..."
  envsubst '${GOOGLE_MAPS_API_KEY}' < /usr/share/nginx/html/index.html > /usr/share/nginx/html/index.tmp
  mv /usr/share/nginx/html/index.tmp /usr/share/nginx/html/index.html
fi
