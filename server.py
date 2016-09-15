#  coding: utf-8 
import SocketServer
import os

# Copyright 2016 Abram Hindle, Eddie Antonio Santos, Xuping Fang
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    fileName=None
    fileType="text/undefined"
    filePath=None
    
    code=-1
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
	print "~~~"
	if(self.checkRequestType(self.extractHeader())==True):
	    self.searchFile(self.extractHeader())
	
	self.sendResponse()
    
    def sendResponse(self):
	
	response=""
	
	if(self.code==200):
	    response="HTTP/1.1 200 OK\r\nContent-Type: "+self.fileType+"\r\n\n"+open(self.filePath).read()
	    
	elif(self.code==404):
	    response="HTTP/1.1 404 Not Found\r\nContent-Type: "+self.fileType+"\r\n"
	    
	#print response
	
	self.request.sendall(response)
    
    def checkRequestType(self,header):
	if(header.split()[0]=="GET" and header.split()[2]=="HTTP/1.1"):
	    return True
	return False
	
    def searchFile(self,header):
	
	self.filePath="www"+header.split()[1]
	
	if(self.filePath[len(self.filePath)-1]=="/" and os.path.isdir(self.filePath[:len(self.filePath)-1])):
	    self.filePath=self.filePath+"index.html"
	
	if(os.path.isfile(self.filePath)):
	    self.fileName=self.filePath.split("/")[len(self.filePath.split("/"))-1]
	    if("." in self.fileName):
		currentFileType=self.fileName.split(".")[1].lower()
	    
		if(currentFileType=="css" or currentFileType=="html"):
		    self.fileType="text/"+currentFileType
		    self.code=200
		    return
	
	self.code=404
	
	 
    def extractHeader(self):
	requestList=self.data.split('\r\n')
	header=requestList[0]
	return header
    

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
