from flask import Flask
from flask import request, jsonify
import time

def getRequestType(headers):
	requestHeaders = dict(headers)
	return requestHeaders['Content-Type']

#defines an object for the application
app = Flask(__name__)

#Creates in-memory data store for the messages
messageStore = [
{
	'id' : 1111111111,
	'message': "Welcome to Qlik message store"
}
]

def generateResponse(status, action, info=None, error=None, response=None):
	responsedata = {
		'status' : status,
		'action' : action,
		'info' : info,
		'error' : error,
		'response' : response
	}
	return jsonify(responsedata)

#Allows the user to post messages to the store using the HTTP POST method
@app.route('/api/message', methods=['POST'])
def addMessage():
	if getRequestType(request.headers) == 'application/x-www-form-urlencoded':
		requestdata = request.form
	elif getRequestType(request.headers) == 'application/json':
		requestdata = request.json
	else:
		return generateResponse(451, "Add Message", info="Failed", error="Invalid request: Only x-www-form-urlencoded or json")

	if requestdata['message'] is None or requestdata['message'] == "":
		return generateResponse(200, "Add Message", info="Failed", error="No or Blank Message data")

	messageData = {
		'id' : int(time.time()),
		'message' : requestdata['message']
	}
	messageStore.append(messageData)
	return generateResponse(200, "Add Message", info="Success", response=messageData)


#Allows the user to list messages from the store using the HTTP GET method
@app.route('/api/message', methods=['GET'])
def ListMessage():
	return generateResponse(200, "List All Messages", info="Success", response=messageStore)

#Allows the user to retrieve specific message from the store using the HTTP GET method and the message ID
#Palindrome check is implemented
@app.route('/api/message/<msg_id>', methods=['GET'])
def ListSpecificMessage(msg_id):
	my_message = None
	for sMessage in messageStore:
		if sMessage['id'] == int(msg_id):
			my_message = sMessage
			break
	if my_message is not None:
		if my_message['message'] == my_message['message'][::-1]:
			palindrome = "Palindrome Check - Passed"
		else:
			palindrome = "Palindrome Check - Failed"
		return generateResponse(200, "List Specific Message", info="Success::"+palindrome, response=my_message)
	else:
		return generateResponse(404, "List Specific Message", info="Failed", error="Your message id does not exist")

#Allows the user to delete specific message from the store using the HTTP POST method and the message ID
@app.route('/api/message/<msg_id>', methods=['POST'])
def DeleteSpecificMessage(msg_id):
	my_message = None
	for sMessage in messageStore:
		if sMessage['id'] == int(msg_id):
			my_message = sMessage
			break
	if my_message is not None:
		messageStore.remove(my_message)
		return generateResponse(200, "Delete Specific Message", info="Success", response=my_message)
	else:
		return generateResponse(404, "Delete Specific Message", info="Failed", error="Your message id does not exist")

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)
