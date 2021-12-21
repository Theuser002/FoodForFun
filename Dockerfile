FROM nvcr.io/nvidia/tensorflow:21.11-tf2-py3

WORKDIR /comvis
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./foodforfun/comvis-components/model .
CMD [ "python3", "model2.py" ]