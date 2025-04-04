FROM nginx:1.25-alpine

# Add a build argument for cache busting
ARG CACHEBUST=1

# Remove default nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf
COPY django.conf /etc/nginx/conf.d/django.conf

# Create directory for static files
RUN mkdir -p /static

# Verify the configuration
RUN echo "Verifying nginx configuration with upstream django and frontend"
RUN cat /etc/nginx/conf.d/django.conf
RUN nginx -t

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]