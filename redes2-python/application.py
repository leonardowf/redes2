import logger
import server
import client

from datetime import datetime

t = datetime.time(datetime.now())
l = logger.LoggerHTML("banana.html")
f = logger.LoggerFile("banana.txt")
x = logger.Logger()
l.log(t, "mensagem")
f.log(t, "mensagem")
x.log(t, "outra")


