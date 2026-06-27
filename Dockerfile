FROM python:3.11-slim

WORKDIR /app

# Copy files
COPY requirements.txt .
COPY streamlit_app.py .
COPY app/ ./app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 7860

# Run Streamlit
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=7860", "--server.address=0.0.0.0"]