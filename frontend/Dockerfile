# Step 1: Use an official Node.js runtime as a parent image
FROM node:16-alpine as build-stage

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the app for production
RUN npm run build

# Step 2: Use an Nginx server to serve the Vue.js app
FROM nginx:alpine

# Copy the built files from the previous stage to the Nginx container
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]
