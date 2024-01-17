# Usa un'immagine di base di Python
FROM python:3.12-alpine

# Imposta la directory di lavoro nel contenitore
WORKDIR /app

# Copia i file di dipendenza
COPY requirements.txt .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice sorgente nell'immagine
COPY app/ .

# Specifica il comando di avvio dell'applicazione
CMD ["python", "main.py"]
