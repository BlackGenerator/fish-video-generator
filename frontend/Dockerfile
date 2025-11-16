# 构建阶段
FROM node:24-alpine AS builder

WORKDIR /app

# 复制依赖清单
COPY package*.json ./

# ✅ 安装 ALL 依赖（包括 devDependencies），因为要运行 vite build
RUN npm ci

# 复制源码
COPY . .

# 执行构建
RUN npm run build

# 生产阶段（仅需静态文件）
FROM nginx:alpine

# 从构建阶段复制生成的静态文件
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制 Nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]