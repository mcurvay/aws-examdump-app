# Multi-stage build for AWS SAA-C03 Exam Practice App
FROM nginx:alpine

# Metadata
LABEL maintainer="AWS SAA-C03 Exam App"
LABEL description="Interactive AWS SAA-C03 exam practice application with spaced repetition"

# Copy application files
COPY index.html /usr/share/nginx/html/
COPY style.css /usr/share/nginx/html/
COPY app.js /usr/share/nginx/html/
COPY questions.json /usr/share/nginx/html/

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost/health || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]

