# Build stage
FROM node:20-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# Runtime stage
FROM node:20-alpine
WORKDIR /app

# Copy from builder
COPY --from=builder /app /app

# Install dependencies
RUN npm install

EXPOSE 3000
CMD ["node", "server.js"]
