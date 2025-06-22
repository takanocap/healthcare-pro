FROM node:20-bullseye-slim AS build

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm install --save-dev @vite-pwa/assets-generator sharp sharp-ico

RUN npm run build

ARG VITE_API_URL

FROM nginx:stable-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD [ "nginx", "-g", "daemon off;" ]

# FROM node:20-slim AS serve
# WORKDIR /app
# RUN npm install -g serve
# COPY --from=build /app/dist ./dist

# CMD ["serve", "-s", "dist", "-l", "4000"]
# FROM node:20-slim AS build

# WORKDIR /app

# COPY package*.json ./

# RUN npm install 

# COPY . .

# RUN npm run build

# FROM nginx:alpine

# # If your build output is in 'dist', update the path below accordingly
# COPY --from=build /app/dist /usr/share/nginx/html

# EXPOSE 80

# CMD [ "nginx", "-g", "daemon off;" ]