# Stage 1: Build the Next.js application
FROM node:22-alpine AS builder

# Set working directory inside the container
WORKDIR /app

# Copy only package.json and package-lock.json to leverage Docker layer caching
COPY package*.json ./

# Install all dependencies (including dev dependencies needed for build)
RUN npm install

# Copy the rest of the source code into the container
COPY . .

# Build the Next.js app for production, generating optimized files in .next/
RUN npm run build

# Stage 2: Create the production image with minimal files
FROM node:22-alpine

# Set working directory inside the container
WORKDIR /app

# Declare build argument
ARG NEXT_PUBLIC_BACKEND_URL
# Set environment variable for build process
ENV NEXT_PUBLIC_BACKEND_URL=${NEXT_PUBLIC_BACKEND_URL:-/api}

# Copy only the package.json files (if needed, e.g., for metadata or running scripts)
COPY --from=builder /app/package*.json ./

# Copy installed node_modules from builder stage to keep production dependencies
COPY --from=builder /app/node_modules ./node_modules

# Copy the built Next.js files from the builder stage
COPY --from=builder /app/.next ./.next

# Copy the public folder containing static assets
COPY --from=builder /app/public ./public

# Expose port 3000 to access the Next.js server externally
EXPOSE 3000
# Set environment variable for production
ENV NODE_ENV=production 

# Command to start the Next.js production server
CMD ["npm", "start"]
