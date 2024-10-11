import grpc
import def_pb2
import def_pb2_grpc

class Client():
  def __init__(self, host = 'localhost', port = 50051):
    self.host = host
    self.port = port
    self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')
    self.stub = def_pb2_grpc.ServiceStub(self.channel)
  
  def greet(self, name):
    request = def_pb2.GreetRequest(name = name)
    response = self.stub.Greet(request)
    return response.message

if __name__ == '__main__':
  client = Client()
  print(client.greet('Håkon'))