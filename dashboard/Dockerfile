FROM python

RUN mkdir /service
COPY protobufs/ /service/protobufs/
COPY dashboard/ /service/dashboard/
WORKDIR /service/dashboard
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/sensor.proto
EXPOSE 5000
ENV FLASK_APP=dashboard.py
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0"]