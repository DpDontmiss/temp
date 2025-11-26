FROM python:3.11-slim

# Install LibreOffice and other system dependencies
# We need default-jre for LibreOffice to work fully in some cases, though headless might be fine without it.
# Adding procps for ps command if needed.
RUN apt-get update && apt-get install -y \
    libreoffice \
    default-jre \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Install Python libraries
RUN pip install --no-cache-dir \
    odfpy \
    pandas \
    openpyxl \
    pyexcel-ods \
    mcp

# Create a working directory
WORKDIR /sandbox

# Default command (can be overridden)
CMD ["python3"]
