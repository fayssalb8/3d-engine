# Machine Shop Suite - 3D Printing Quote Engine
# Multi-stage Docker build for production

FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies and PrusaSlicer
# PrusaSlicer AppImage needs GTK3 and OpenGL libraries even for CLI mode
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    ca-certificates \
    libgl1 \
    libglib2.0-0 \
    libgtk-3-0 \
    libgomp1 \
    libxrender1 \
    libxext6 \
    libx11-6 \
    libxcb1 \
    libfontconfig1 \
    libsm6 \
    libice6 \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libxi6 \
    libxcursor1 \
    libxtst6 \
    libwayland-client0 \
    libwayland-egl1 \
    && rm -rf /var/lib/apt/lists/*

# Download and install PrusaSlicer (AppImage)
# Using version 2.8.1 - last stable version with AppImage (2.9.x moved to Flatpak)
# Note: 2.8.1 has SLA support via --export-sla command
RUN wget "https://github.com/prusa3d/PrusaSlicer/releases/download/version_2.8.1/PrusaSlicer-2.8.1%2Blinux-x64-newer-distros-GTK3-202409181416.AppImage" \
    -O /usr/local/bin/PrusaSlicer.AppImage \
    && chmod +x /usr/local/bin/PrusaSlicer.AppImage

# Extract AppImage (since AppImage needs FUSE which doesn't work well in Docker)
RUN cd /usr/local/bin \
    && ./PrusaSlicer.AppImage --appimage-extract \
    && ln -s /usr/local/bin/squashfs-root/usr/bin/prusa-slicer /usr/local/bin/prusa-slicer \
    && rm PrusaSlicer.AppImage

# Create app directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY config.py .
COPY utils.py .
COPY templates/ ./templates/
COPY static/ ./static/

# Create necessary directories with proper permissions
RUN mkdir -p logs uploads

# Create non-root user for security and set ownership
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Health check - use curl to check our health endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "300", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
