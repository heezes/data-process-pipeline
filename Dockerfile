FROM ubuntu
ARG GITUSER
ARG GITPASS

FROM ubuntu
RUN apt-get update 
RUN apt-get -y install python3 
RUN apt-get -y install python3-pip
RUN apt-get -y install git
RUN git clone https://$GITUSER:$GITPASS@github.com/heezes/data-process-pipeline.git 
WORKDIR /data-process-pipeline
RUN pip3 install -r requirements.txt

RUN python3 -m jfwEncoderDecoder.jfw_generator serializer_conf.h

CMD ["python3", "main.py"]