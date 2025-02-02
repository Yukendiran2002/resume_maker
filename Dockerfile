FROM python:3.12-slim

# Install required system libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app

# Set the working directory
WORKDIR /app

# Expose the correct Cloud Run port
EXPOSE 8080

# Command to run the Streamlit app on port 8080
CMD ["sh", "-c", "streamlit run resume_maker.py --server.port=8080 --server.address=0.0.0.0"]
