FROM nvcr.io/nvidia/tensorflow:21.11-tf2-py3

WORKDIR /
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "server.py"]