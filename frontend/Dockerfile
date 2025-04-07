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

# Environment variables
ENV NODE_ENV=production
ENV API_BASE_URL=http://apirest.mibitech.com.br:8000
ENV PORT=3000

# Install production dependencies only
RUN npm install --production

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:3000/ || exit 1

EXPOSE 3000
CMD ["node", "server.js"]