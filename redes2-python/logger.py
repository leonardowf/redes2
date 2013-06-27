# coding=UTF-8

import os

# Define a class Logger e classes relacionadas
# Um Logger implementa o método log(time, message)
# Para LoggerHTML e LoggerFile um diretório é criado, especificado por log_directory

class Logger:
    log_directory = "log/"
    def __init__(self):
        self.count = 0
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)
    
    def log(self, time, message):
        print "<#%d>" % self.count + "\t" + "<%s>" % time + "\t" + message
        self.count = self.count + 1

class LoggerHTML(Logger):
    def __init__(self, file_name):
        Logger.__init__(self)
        self.file_descriptor = open(self.log_directory + file_name, "w")
        self.write_html_header()
        
    def write_html_header(self):
        self.file_descriptor.write("<html>")
        self.file_descriptor.write("<head>")
        self.file_descriptor.write("<body>")
    
    def log(self, time, message):
        a_message = "<p>" + message + "</p>"
        self.file_descriptor.write(a_message)
        self.count = self.count + 1

class LoggerFile(Logger):
    def __init__(self, file_name):
        Logger.__init__(self)
        self.file_descriptor = open(self.log_directory + file_name, "w")
    
    def log(self, time, message):
        a_message = "<#%d>" % self.count + "\t" + "<%s>" % time + "\t" + message + "\n"
        self.file_descriptor.write(a_message)
        self.count = self.count + 1
