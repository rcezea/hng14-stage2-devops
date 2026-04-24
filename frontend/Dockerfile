# Stage 1: builder
FROM node:24-alpine AS builder

WORKDIR /opt/frontend

RUN apk add --no-cache curl=8.17.0-r1

COPY package.json .
RUN npm install

COPY . .


# Stage 2: runtime
FROM node:24-alpine

WORKDIR /opt/frontend

RUN apk add --no-cache curl=8.17.0-r1

# Copy only what we need
COPY --from=builder /opt/frontend /opt/frontend

RUN adduser -D appuser && chown -R appuser:appuser /opt/frontend
USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
CMD curl -f http://localhost:3000/api/health || exit 1

CMD ["node", "app.js"]