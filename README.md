uvicorn main:app --reload --host 0.0.0.0 --port 8443 \
    --ssl-certfile certs/cert.pem --ssl-keyfile certs/key.pem
