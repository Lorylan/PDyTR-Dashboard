import grpc
import sensor_pb2
import sensor_pb2_grpc
from concurrent import futures
import random
import time

class HumSensor(sensor_pb2_grpc.SensorServicer):
  def getData(self, request, context):
    lista= []
    lista.append(random.randint(1,100))
    while (len(lista) != 0):
      yield sensor_pb2.SensorResponse(value=lista[len(lista)-1])
      lista.pop()
      time.sleep(1)
      lista.append(random.randint(1,100))

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  sensor_pb2_grpc.add_SensorServicer_to_server(HumSensor(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  server.wait_for_termination()

if __name__ == '__main__':
  serve()


  