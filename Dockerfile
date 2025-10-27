FROM python:3.12-slim

# No buffering log
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install UV e compile deps prod-ready
RUN pip install --no-cache-dir uv

# Copy and install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# Copy the code
COPY app ./app

# Expose port
EXPOSE 8080

CMD ["uv", "run", "fastapi", "dev", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
