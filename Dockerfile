FROM ubuntu

RUN apt-get update 
RUN apt-get -y install python3 
RUN apt-get -y install python3-pip

COPY . .

RUN pip3 install -r requirements.txt

RUN python3 -m jfwEncoderDecoder.jfw_generator serializer_conf.h

CMD ["python3", "main.py"]