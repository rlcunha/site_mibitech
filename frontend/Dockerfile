# Build stage
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .

# Runtime stage
FROM node:20-alpine
WORKDIR /app
ENV NODE_ENV=production

# Copy only necessary files from builder
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/views ./views
COPY --from=builder /app/controllers ./controllers
COPY --from=builder /app/models ./models
COPY --from=builder /app/server.js ./

# # Health check
# HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
#   CMD curl -f https://appteste.mibitech.com.br/health || exit 1

EXPOSE 3000
CMD ["node", "server.js"]
