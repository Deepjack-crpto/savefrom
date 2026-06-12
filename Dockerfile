# Use the official Node.js Alpine base image for a lightweight runtime
FROM node:18-alpine

# Install essential system dependencies including Python3, ffmpeg, curl
RUN apk update && \
    apk add --no-cache python3 ffmpeg curl bash

# Download and install yt-dlp globally
RUN curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp && \
    chmod a+rx /usr/local/bin/yt-dlp

# Set the application directory
WORKDIR /app

# Copy dependency mappings
COPY package*.json ./

# Install Node dependencies
RUN npm install

# Copy application files
COPY . .

# Expose standard port
EXPOSE 3000

# Start server
CMD ["node", "server.js"]
