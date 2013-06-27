# coding=UTF-8

import logger
import server
import client

html = logger.LoggerHTML("testehtml.html")
txt1 = logger.LoggerFile("teste1.txt")
txt2 = logger.LoggerFile("teste2.txt")
x = logger.Logger()

c = client.Client()
c.add_logger(html)
c.add_logger(txt1)
c.add_logger(txt2)
c.add_logger(x)

c.log("as mensagens vão para todos os logs")
c.log("e como se todos fossem 'observers'")
c.log("mas não são")



