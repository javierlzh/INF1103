FROM python:3.11-slim 

WORKDIR /usr/src/app

COPY inventory_manager.py .
COPY inventory.json .

CMD ["python", "inventory_manager.py"]
