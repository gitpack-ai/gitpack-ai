# Use Node.js 22.9.0 as the base image
FROM node:22.9.0-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the rest of the frontend application code
COPY . /app/

# Install dependencies
RUN npm ci

# Build the Next.js application
RUN npm run build

# Expose the port that the application will run on
EXPOSE 3000

# Start the application
CMD ["npm", "start"]


