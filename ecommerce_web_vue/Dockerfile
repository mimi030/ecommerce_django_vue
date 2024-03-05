# For Development

# Build stage
# Pull official base image
# FROM node:18-alpine as build-stage
FROM node:18-alpine AS development

# Update npm to the latest version
RUN npm install -g npm@latest

# Set work directory
WORKDIR /usr/src/frontend

# Install Vue CLI globally
RUN npm install -g @vue/cli

# Copy both 'package.json' and 'package-lock.json'
COPY ./package*.json ./

# Install project dependencies 
RUN npm install

# Copy project files and folders to the current working directory
COPY . .

# Expose the HTTP port
EXPOSE 8080

# Change the ownership of the 'node_modules' directory
# and its contents to the 'node' user
RUN chown -R node ./node_modules

# Set the user to node (non-root) to avoid permission issue
USER node

# Start serving requests
CMD [ "npm", "run", "serve" ]