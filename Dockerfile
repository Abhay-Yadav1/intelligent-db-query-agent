FROM python:3.11-slim

WORKDIR /app

# Copy only what's needed
COPY backend/ ./backend/
COPY agents/ ./agents/
COPY database/ ./database/
COPY graphs/ ./graphs/
COPY utils/ ./utils/
COPY data/ ./data/
COPY main.py ./
COPY config.py ./
COPY .env ./

# Install dependencies
RUN pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn[standard]==0.24.0 \
    pydantic==2.5.0 \
    langchain==0.1.0 \
    langchain-groq==0.0.1 \
    langgraph==0.0.20 \
    sqlalchemy==2.0.23 \
    python-dotenv==1.0.0

# Expose port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]