# ------------ 1. Build Frontend ------------
FROM node:18 AS frontend

WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend .
RUN npm run build


# ------------ 2. Setup Python Backend ------------
FROM python:3.10-slim AS backend

WORKDIR /app

# Install backend dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend ./backend

# Copy built frontend into backend static files
COPY --from=frontend /app/frontend/dist ./frontend_dist

# Install production server
RUN pip install uvicorn python-multipart

# Expose port
EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
