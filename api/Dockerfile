FROM python:3.11-slim

WORKDIR /opt/api

#RUN apt-get update && apt-get install --no-install-recommends -y curl=8.14.1-2+deb13u2 && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

# Upgrade Python tooling (fixes pip/wheel CVEs)
# hadolint ignore=DL3013
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m hngdevops
USER hngdevops

EXPOSE 8000

#HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
#CMD curl -f http://api:8000/api/health || exit 1

# Healthcheck without curl
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
CMD python -c "import urllib.request; urllib.request.urlopen('http://api:8000/api/health')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# version pinning makes code reproducible
# --no-install-recommends avoids installing unnecessary packages
# apt-cache policy curl to check installed version

# Commented out and replaced actions leading to vulnerabilities
