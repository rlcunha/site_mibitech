# Build stage
FROM node:20-alpine AS builder

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

# Health check - teste de sanidada
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:3000/ || exit 1

EXPOSE 3000
CMD ["node", "server.js"]
