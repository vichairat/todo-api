from flask import Flask, Response, request
app = Flask(__name__)

import json
import TodoDB

@app.route("/")
def index():
    return "Todo API is running. Sample http://localhost:5000/api/todo"

#GET /api/todo
@app.route("/api/todo", methods=['GET'])	
def getAll():
	
	rows = TodoDB.conn.execute('SELECT id, subject, detail, done FROM items ORDER BY id ASC')
	d = {}
	d['status'] = 200
	d['error'] = None	
	d['items'] = []
	for row in rows:
		item = {}
		item['id'] = row[0]
		item['subject'] = row[1]
		item['detail'] = row[2]
		item['done'] = row[3]
		d['items'].append(item)

	return Response(json.dumps(d), mimetype='application/json')
	
#GET /api/todo/{id}
@app.route("/api/todo/<int:id>", methods=['GET'])	
def getById(id):
	rows = TodoDB.conn.execute('SELECT id, subject, detail, done FROM items WHERE id = %d'%id)
	d = {}
	d['status'] = 404
	d['error'] = 'Not found item id %d'%id
	count = 0
	item = None
	for row in rows:
		count = count + 1
		item = {}
		item['id'] = row[0]
		item['subject'] = row[1]
		item['detail'] = row[2]
		item['done'] = row[3]
		d['item'] = item

	if count > 0:
		d['status'] = 200
		d['error'] = None

	return Response(json.dumps(d), mimetype='application/json')

#POST /api/todo
@app.route("/api/todo", methods=['POST'])
def addItem():
	d = {}
	
	try:
		item = request.get_json(force=True)		
	except:
		d['status'] = 400
		d['error'] = 'Bad Request, We accept only json for this request.'
		return Response(json.dumps(d), mimetype='application/json')
			
	insertScript = ''
	try:				
		insertScript = "INSERT INTO items(subject, detail, done) VALUES('%s', '%s', %d)" % (item['subject'], item['detail'], item['done'])
		
	except:
		d['status'] = 400
		d['error'] = 'Bad Request, incorrect input task format.'
		return Response(json.dumps(d), mimetype='application/json')
	
	cursor = TodoDB.conn.cursor()
	cursor.execute(insertScript)
	item['id'] = cursor.lastrowid
	d['item'] = item
	TodoDB.conn.commit()
	
	d['status'] = 200
	d['error'] = None
	return Response(json.dumps(d), mimetype='application/json')

#PUT /api/todo/{id}
@app.route("/api/todo/<int:id>", methods=['PUT'])
def updateItem(id):
	d = {}
	
	try:
		item = request.get_json(force=True)		
	except:
		d['status'] = 400
		d['error'] = 'Bad Request, We accept only json for this request.'
		return Response(json.dumps(d), mimetype='application/json')
			
	updateScript = ''
	try:				
		updateScript = "UPDATE items SET subject='%s', detail='%s', done=%d WHERE id = %d" % (item['subject'], item['detail'], item['done'], id)
	except:
		d['status'] = 400
		d['error'] = 'Bad Request, incorrect input task format.'
		return Response(json.dumps(d), mimetype='application/json')
	
	#item id exist?
	rows = TodoDB.conn.execute("SELECT id FROM items WHERE id = %d"%id)
	count = 0
	for row in rows:
		count = count + 1
	
	if count > 0:
		TodoDB.conn.execute(updateScript)
		TodoDB.conn.commit()
		d['status'] = 200
		d['error'] = None
	else:
		d['status'] = 404
		d['error'] = 'Not found item id %d'%id
		
	return Response(json.dumps(d), mimetype='application/json')
	

#DELETE /api/todo/{id}
@app.route("/api/todo/<int:id>", methods=['DELETE'])
def deleteItem(id):
	d = {}
	
	#item id exist?
	rows = TodoDB.conn.execute("SELECT id FROM items WHERE id = %d"%id)
	count = 0
	for row in rows:
		count = count + 1
	
	if count > 0:
		TodoDB.conn.execute("DELETE FROM items WHERE id=%d"%id)
		TodoDB.conn.commit()
		d['status'] = 200
		d['error'] = None
	else:
		d['status'] = 404
		d['error'] = 'Not found item id %d'%id
		
	return Response(json.dumps(d), mimetype='application/json')
	


if __name__ == "__main__":
    app.run()

	
	
	
	
	
	
	
	
	