import grpc
from concurrent import futures
import time
import def_pb2
import def_pb2_grpc

class Server():
  def __init__(self):
    pass

  def Greet(self, request, context):
    response = def_pb2.GreetResponse()
    print(f"Greeting {request.name}")
    response.message = f'Hello, {request.name}'
    return response
  
def start_server(port = 50051):
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  def_pb2_grpc.add_ServiceServicer_to_server(Server(), server)
  server.add_insecure_port(f'[::]:{port}')
  server.start()

  try:
    while True:
        time.sleep(86400)
  except KeyboardInterrupt:
      server.stop(0)

if __name__ == '__main__':
  start_server()