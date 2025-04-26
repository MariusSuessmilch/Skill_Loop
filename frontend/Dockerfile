# --- Build stage ---
FROM node:20 as build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install --include=dev && npm install @vitejs/plugin-vue@4
COPY . .
RUN npm run build

# --- Production stage (for Cloud Run) ---
FROM node:20 as prod
WORKDIR /app
COPY --from=build /app/dist ./dist
RUN npm install -g serve
EXPOSE 8080
CMD ["serve", "-s", "dist", "-l", "8080"]

# --- Dev stage: for local development (optional) ---
# To use: docker build --target dev -t code-coach-frontend-dev . && docker run -p 5173:5173 code-coach-frontend-dev
FROM node:20 as dev
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install --include=dev && npm install @vitejs/plugin-vue@4
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]