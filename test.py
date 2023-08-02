from client import Client

client = Client(['localhost:5000', 'localhost:5001', 'localhost:5002'])
client.add('mykey', 'myvalue')
print(client.get('mykey'))  # Should print 'myvalue'
client.delete('mykey')
print(client.get('mykey'))  # Should print 'None'