FROM node:24-alpine

WORKDIR /opt/frontend

RUN apk add --no-cache curl

COPY package.json .
RUN npm install

COPY . .

RUN adduser -D hngdevops && chown -R hngdevops:hngdevops /opt/frontend
USER hngdevops

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
CMD curl -f http://localhost:3000/api/health || exit 1

CMD ["node", "app.js"]
