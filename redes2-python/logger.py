class Logger:
    def __init__(self):
        self.count = 0
    
    def log(self, time, message):
        print "<#%d>" % self.count + "\t" + "<%s>" % time + "\t" + message
        self.count = self.count + 1

class LoggerHTML(Logger):
    def __init__(self, file_name):
        Logger.__init__(self)
        self.file_descriptor = open("log/" + file_name, "w")
        self.write_html_header()
        
    def write_html_header(self):
        self.file_descriptor.write("<html>")
        self.file_descriptor.write("<head>")
        self.file_descriptor.write("<body>")
    
    def log(self, time, message):
        a_message = "<p>" + message + "</p>"
        self.file_descriptor.write(a_message)

class LoggerFile(Logger):
    def __init__(self, file_name):
        Logger.__init__(self)
        self.file_descriptor = open("log/" + file_name, "w")
    
    def log(self, time, message):
        a_message = "<#%d>" % self.count + "\t" + "<%s>" % time + "\t" + message
        self.file_descriptor.write(a_message)
