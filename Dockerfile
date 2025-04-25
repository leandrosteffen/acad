FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg \
    chromium-driver chromium \
    libxml2-dev libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV CHROME_BIN=/usr/bin/chromium
ENV PATH="/usr/lib/chromium:$PATH"

CMD ["bash", "-c", "python webdownload.py && streamlit run sisteminha.py --server.port 80 --server.enableCORS false"]