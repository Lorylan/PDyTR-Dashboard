# PDyTR-Dashboard
Trabajo final de la materia Programación Distribuida y Tiempo Real

### Alumnos

Jacinto, Milagros Aylén - Nº de alumno: 15938/5

Moschettoni, Martín - Nº de alumno: 15836/0

---

## Indice

1. [Aplicación realizada](#app)
2. [Desarrollo](#desarrollo)
3. [Directorios](#dirs)
4. [Servidores gRPC](#servers)
5. [Dashboard](#dashboard)
6. [Docker](#docker)
7. [Ejecución](#run)
8. [¿Cómo usar la aplicación?](#uso)
9. [Referencias](#ref)

<a name="app"></a>
## Aplicación realizada

La aplicación construida es un dashboard con información obtenida de tres servicios gRPC que simulan ser sensores de temperatura, luminosidad y humedad. El dashboard se comunica con cada servidor y recibe un stream de datos que muestra en tiempo real a los usuarios conectados al servidor web donde el dashboard reside. 

Se utilizó Python para la construcción de los servidores gRPC y Flask para el dashboard, y se utilizó Docker para contener ambas funcionalidades.

![Figura 1: Flujo de comunicación entre los servidores y el dashboard](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/426fa5aa-692d-4310-b516-2fc08f277ad5/Dashboard.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220926%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220926T193857Z&X-Amz-Expires=86400&X-Amz-Signature=a49e8214e44441ff71d4453236f3a55916abf26c8f7bc73caf65216aa09c1a96&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Dashboard.png%22&x-id=GetObject)

Figura 1: Flujo de comunicación entre los servidores y el dashboard

<a name="desarrollo"></a>
# Desarrollo

El desarrollo comenzó analizando la referencia proporcionada por la cátedra, donde se explica una versión similar a la construida pero con sólo un servidor gRPC que retorna múltiples mediciones de distintos sensores.

Se decidió utilizar Python para el desarrollo de los servidores gRPC porque es un lenguaje con el cual se tuvo experiencia previa además de que se buscó evitar copiar al pie de la letra lo que la referencia realizaba.

También se cambio React (que se usaba en la referencia) por Flask, nuevamente para evitar copiar el código y explicación, pero además porque facilita el utilizar gRPC con Python, ya que no es necesario utilizar Envoy como en la referencia.

<a name="dirs"></a>
## Directorios

- Se crearon las carpetas sensors (para guardar los servidores gRPC), dashboard (donde se encuentra la aplicación de Flask) y protobuf (donde se guarda el .proto)
- Dentro de la carpeta protobuf se creó el archivo Sensor.proto para definir la interfaz de los servidores gRPC
- En la carpeta dashboard se crearon los archivos dashboard.py (la aplicación que se ejecuta en Flask) y requirements.txt (requerimientos para Flask y gRPC).
- En dashboard además se creó la carpeta static y dentro de la misma la carpeta css, allí se creó el archivo homepage.css.
- Dentro de dashboard se creo la carpeta template y dentro de la misma se creo el archivo homepage.html que sera la página única y principal de la aplicación.
- Luego se creo el entorno virtual necesario para Flask con los siguientes comandos:
    
    ```bash
    python -m venv venv
    source venv/Scripts/activate
    ```
    
- Los directorios quedaron con la siguiente estructura:

```
├── dashboard/
│   ├── dashboard.py
│   ├── requirements.txt
│ 	├── sensor_pb2.py
│   ├── sensor_pb2_grpc.py
│ 	├── static/
│   |    └── css/
│   |        └── homepage.css
│   └── templates/
│       └── homepage.html
|
└── sensors/
    ├── serviceHum.py
    ├── serviceLum.py
    ├── serviceTemp.py
    ├── sensor_pb2.py
    ├── sensor_pb2_grpc.py
    └── requirements.txt
```

<a name="servers"></a>
## Servidores gRPC

Se definió la interfaz en el archivo Sensor.proto:

```protobuf
synyax="proto3";

message Empty{}

message SensorResponse{
	int64 value = 1;
}

service Sensor{
	rpc getData(Empty) returns (stream SensorResponse){};
}
```

La idea es que el “cliente” (el dashboard) envíe un mensaje vacío y reciba como respuesta un stream con los valores que el sensor va “obteniendo”.

- Se creo el archivo requirements.txt dentro de la carpeta sensors donde se especificó como requerimiento “grpcio-tools”, que son las herramientas de gRPC en Python. Allí se encuentra la herramienta Protoc y se instaló con el siguiente comando:
    
    ```bash
    python -m pip install -r sensors/requirements.txt 
    ```
    
- Una vez instalada la herramienta Protoc se la utiliza para generar los archivos Python que contendrán las clases necesarias para realizar la comunicación gRPC.

```python
cd sensors #Ingresa a la carpeta sensors donde estaran los servidores gRPC
python -m grpc_tools.protoc -I ../protobufs --python_out=. \
>          --grpc_python_out=. ../protobufs/sensor.proto
```

- A partir del archivo Sensor.proto crea dos archivos “sensor_pb2” y “sensor_pb2_grpc” ambos necesarios para la funcionalidad completa de los servidores gRPC.
- Se crearon tres archivos llamados serviceHum, serviceLum y serviceTemp, uno para cada sensor y tienen la siguiente funcionalidad:

```python
import grpc
import sensor_pb2
import sensor_pb2_grpc
from concurrent import futures
import random
import time

class Sensor(sensor_pb2_grpc.SensorServicer): #El sensor especifico que cada servidor utiliza
  def getData(self, request, context):
    lista= []
    lista.append(random.randint(1,100))
    while (len(lista) != 0):
      yield sensor_pb2.SensorResponse(value=lista[len(lista)-1])
      lista.pop()
      time.sleep(t)
      lista.append(random.randint(1,100))

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  sensor_pb2_grpc.add_SensorServicer_to_server(Sensor(), server) 
  server.add_insecure_port('[::]:50051')
  server.start()
  server.wait_for_termination()

if __name__ == '__main__':
  serve()
```

Cada sensor tiene como prefijo en el nombre de clase la métrica que esta midiendo, por lo que las clases se llaman HumSensor, LumSensor y TempSensor.

Las clases heredan de SensorServicer, clase que proviene de “sensor_pb2.grpc”.

Para la linea “time.sleep(t)” el valor de t depende del sensor, HumSensor tiene un sleep de 1, LumSensor tiene sleep de 2, y TempSensor sleep de 3. Esto es para que sea mas interesante la construcción de la comunicación ya que los servidores gRPC no envían datos por el stream con la misma frecuencia.

<a name="dashboard"></a>
## Dashboard

- Se instalaron en dashboard los requerimientos necesarios:
    
    ```bash
    python -m pip install -r dashboard/requirements.txt
    ```
    
- Luego se crearon nuevamente las clases con Protoc pero esta vez para usarlas en el dashboard y crear el “cliente” que se comunica con los servidores gRPC:

```bash
cd dashboard
python -m grpc_tools.protoc -I ../protobufs --python_out=. \
         --grpc_python_out=. ../protobufs/sensor.proto
```

- Para que la actualización de los datos ocurra en tiempo real se utilizó la librería Turbo-Flask que permite integrar la librería turbo.js a la aplicación de Flask.
- Turbo-Flask realiza una conexión con un WebSocket del dashboard a los clientes conectados, esta conexión es transparente a la aplicación y es bidireccional. Utilizando un método de la librería llamado “push” se puede enviar por el WebSocket actualizaciones de la página a los usuarios conectados al dashboard.
- En Flask se pueden crear hilos en los cuales se desarrollan las comunicaciones con los distintos servidores gRPC, una vez que la comunicación ocurre se puede utilizar Turbo-Flask para que cada hilo envíe a los usuarios la información que acaba de obtener del servidor gRPC al que se está comunicando.
- Para que los hilos no se superpongan enviando información simultáneamente se utilizó un lock para que solo un hilo a la vez envíe datos actualizados a los clientes conectados.
- En la figura 2 se puede ver el diagrama de la comunicación completa de la aplicación.

![Figura 2: Diagrama de la comunicación completa de la aplicación](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/9cd34806-8280-42eb-aec3-91e3159dba03/Diagrama.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220926%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220926T193918Z&X-Amz-Expires=86400&X-Amz-Signature=33340f89c2d0123a8809a9ea8b18b751602b4c9738ab1515e22c6f2d0845e356&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Diagrama.png%22&x-id=GetObject)

Figura 2: Diagrama de la comunicación completa de la aplicación

<a name="docker"></a>
## Docker

Para poder ejecutar la aplicación en Docker se crearon dos imagenes. 

1. Una de las imagenes contendrá todo lo referente a la aplicación/página web del dashboard. Para ello se creó un archivo Dockerfile dentro de la carpeta dashboard.  

```docker
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
```

1. La otra imagen contendrá los servidores gRPC de temperatura, humedad y luminosidad. Para ello se creó un archivo Dockerfile dentro de la carpeta sensors.

```docker
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
```

<aside>
❔ Se crearon dos imágenes para desacoplar las funcionalidades y que en caso de que se utilice a futuro no sea un inconveniente.

</aside>

Luego de crear las imagenes, se creó un archivo YAML, llamado *docker-compose.yaml* colocado en la raiz del proyecto para crear las imagenes, crear la red de comunicacion dentro de Docker y ejecutar los contenedores.

```yaml
version: "3.8"
services:
  dashboard:
    build:
      context: .
      dockerfile: dashboard/Dockerfile
    environment:
      SENSOR_HOST: sensors
    image: dashboard
    networks:
      - microservices
    ports:
      - 5000:5000

  sensors:
    build:
      context: .
      dockerfile: sensors/Dockerfile
    image: sensors
    networks:
      - microservices
    ports:
      - 50051:50051
      - 50052:50052
      - 50053:50053
networks:
  microservices:
```

Luego de crear los archivos esta es la estructura final de los directorios:

```
.
├── dashboard/
│   ├── dashboard.py
│   ├── requirements.txt
│ 	├── sensor_pb2.py
│   ├── sensor_pb2_grpc.py
│ 	├── Dockerfile
│ 	├── static/
│   |    └── css/
│   |        └── homepage.css
│   └── templates/
│       └── homepage.html
|
├── protobufs/
│   └── sensor.proto
|
├── sensors/
│   ├── serviceHum.py
│   ├── serviceLum.py
│   ├── serviceTemp.py
│   ├── sensor_pb2.py
│   ├── sensor_pb2_grpc.py
│   ├── Dockerfile
│   └── requirements.txt
└── docker-compose.yaml
```

Y para crear las imágenes se ejecutó el siguiente comando:

```bash
docker-compose build
```

---

<a name="run"></a>
## Ejecución

Finalmente para iniciar la aplicación construida se debe ejecutar el siguiente comando:

```bash
docker-compose up
```

Luego se ingresa al enlace proporcionado por la consola (en este caso especifico es localhost:5000) y se podra acceder a la aplicación.

---

<a name="uso"></a>
## ¿Cómo usar la aplicación?

Para poder utilizar la aplicación primero se debe clonar el repositorio git donde se encuentra el proyecto con el siguiente comando en consola:

```bash
git clone https://github.com/Lorylan/PDyTR-Dashboard.git
```

Luego se ingresa a la carpeta del repositorio y se ejecuta el siguiente comando en consola para crear las imágenes y la red para la comunicación de las mismas.

```bash
docker-compose build
```

Por último se ejecuta el siguiente comando en consola para crear el contenedor y ejecutarlo:

```bash
docker-compose up
```

<aside>
❔ Si ya se tienen las imágenes correspondientes, solo debe ejecutar el comando *docker-compose up.*

</aside>

Ahora solo se debe ingresar al navegador de preferencia e ingresar a [localhost:5000](http://localhost:5000) para ver la aplicación en funcionamiento:

![Homepage de la aplicación](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/84277e28-7f91-4dc1-8aff-e25161e14914/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220926%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220926T193938Z&X-Amz-Expires=86400&X-Amz-Signature=18b446014fe487c24562fa1819b663116741cd9dcddbdbe158480503eb414938&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22&x-id=GetObject)

Homepage de la aplicación

---

<a name="ref"></a>
# Referencias

[1] "Building a realtime dashboard with reactjs go grpc and envoy", Nirak Fonseka. https://medium.com/swlh/building-a-realtime-dashboard-with-reactjs-go-grpc-and-envoy-7be155dfabfb (acceso en Septiembre de 2022)

[2] Información sobre como trabajar con server streaming en gRPC. https://www.tutorialspoint.com/grpc/grpc_server_streaming_rpc.htm (acceso en Septiembre de 2022)

[3] Información sobre como utilizar gRPC con Python. https://grpc.io/docs/languages/python/ (acceso en Septiembre de 2022)

[4] "Dynamically Update Your Flask Web Pages Using Turbo-Flask", Miguel Grinberg. https://blog.miguelgrinberg.com/post/dynamically-update-your-flask-web-pages-using-turbo-flask (acceso en Septiembre de 2022)

[5] "Python Microservices With gRPC", Dan Hipschman. https://realpython.com/python-microservices-grpc/ (acceso en Septiembre de 2022)

[6] Información sobre la creación de Dockerfiles y uso de Docker-Compose. https://www.docker.com/ (acceso en Septiembre de 2022)

[7] Documentación de Flask. https://flask.palletsprojects.com/en/2.2.x/ (acceso en Septiembre de 2022)
