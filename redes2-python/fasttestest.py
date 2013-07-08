import packet
import client

c = client.Client("127.0.0.1", 9001)
c.send("banana")

