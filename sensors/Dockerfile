FROM python

RUN mkdir /service
COPY protobufs/ /service/protobufs/
COPY sensors/ /service/sensors/
WORKDIR /service/sensors
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/sensor.proto
EXPOSE 50051 50052 50053
ENTRYPOINT ["/bin/sh", "-c", "python serviceHum.py | python serviceLum.py | python serviceTemp.py"]
