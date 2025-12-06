FROM node:20-alpine
WORKDIR /app
COPY package.json ./
COPY tsconfig.json ./
COPY vite.config.ts ./
RUN npm i
COPY src ./src
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

