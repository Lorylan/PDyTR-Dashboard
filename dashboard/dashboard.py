# save this as app.py
import os
from flask import Flask, render_template
import grpc
from sensor_pb2_grpc import SensorStub
from sensor_pb2 import Empty
from turbo_flask import Turbo
import threading
import time

app = Flask(__name__,template_folder='templates')
turbo = Turbo(app)
lock = threading.Lock()
sensor_host = os.getenv("SENSOR_HOST", "localhost")
sensor_hum_channel = grpc.insecure_channel(
    f"{sensor_host}:50051"
)
sensor_hum_client = SensorStub(sensor_hum_channel)

sensor_lum_channel = grpc.insecure_channel(
    f"{sensor_host}:50052"
)
sensor_lum_client = SensorStub(sensor_lum_channel)

sensor_temp_channel = grpc.insecure_channel(
    f"{sensor_host}:50053"
)
sensor_temp_client = SensorStub(sensor_temp_channel)

sensor_hum_request = Empty()
sensor_lum_request = Empty()
sensor_temp_request = Empty()

sensor_hum_response = sensor_hum_client.getData(sensor_hum_request)
sensor_lum_response = sensor_lum_client.getData(sensor_lum_request)
sensor_temp_response = sensor_temp_client.getData(sensor_temp_request)

temperatura = 0
luminosidad = 0
humedad = 0

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_lum).start()
    threading.Thread(target=update_hum).start()
    threading.Thread(target=update_temp).start()

def update_lum():
    global humedad,temperatura,luminosidad
    with app.app_context():
        while True:
            luminosidad=sensor_lum_response.next()
            lock.acquire()
            time.sleep(0.5)
            turbo.push(turbo.replace(render_template('homepage.html',
                    hum=humedad,
                    temp=temperatura,
                    lum=luminosidad, 
                ), 'data'))
            lock.release()
            
def update_hum():
    global humedad,temperatura,luminosidad
    with app.app_context():
        while True:
            humedad=sensor_hum_response.next()
            lock.acquire()
            time.sleep(0.5)
            turbo.push(turbo.replace(render_template('homepage.html',
                    hum=humedad,
                    temp=temperatura,
                    lum=luminosidad, 
                ), 'data'))
            lock.release()
              
def update_temp():
    global humedad,temperatura,luminosidad
    with app.app_context():
        while True:
            temperatura=sensor_temp_response.next()
            lock.acquire()
            time.sleep(0.5)
            turbo.push(turbo.replace(render_template('homepage.html',
                    hum=humedad,
                    temp=temperatura,
                    lum=luminosidad, 
                ), 'data'))  
            lock.release()  

@app.route("/", methods = ['POST', 'GET'])
def inicio():
    global humedad,temperatura,luminosidad
    humedad=sensor_hum_response.next()
    temperatura=sensor_temp_response.next()
    luminosidad=sensor_lum_response.next()
    return render_template(
        'homepage.html',
        hum=humedad,
        lum=luminosidad,
        temp=temperatura
    )

    
if __name__ == "__main__":
    app.run()
else :
    app.config.update(
        APPLICATION_ROOT="/",
        TEMPLATES_AUTO_RELOAD=True
    )