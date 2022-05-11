from app import app, mongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request

@app.route('/api/users', methods=['POST'])
def add_user():
	_json = request.json
	_name = _json['name']
	_dob = _json['dob']
	_address = _json['address']
	_desc = _json['desc']
	# validate the received values
	if _name:
		id = mongo.db.users.insert_one({'name': _name, 'dob': _dob, 'address': _address, 'desc': _desc})
		resp = jsonify('User added successfully!')
		resp.status_code = 200
		return resp
	else:
		return not_found()
		
@app.route('/api/users')
def users():
	users = mongo.db.users.find()
	resp = dumps(users)
	return resp
		
@app.route('/api/users/<id>')
def user(id):
	user = mongo.db.users.find_one({'_id': ObjectId(id)})
	resp = dumps(user)
	return resp

@app.route('/api/users/<id>', methods=['PUT'])
def update_user(id):
	_json = request.json
	_name = _json['name']
	_dob = _json['dob']
	_address = _json['address']
	_desc = _json['desc']
	if _name and id and request.method == 'PUT':
		mongo.db.users.update_one({'_id': ObjectId(id['$oid']) if '$oid' in id else ObjectId(id)}, {'$set': {'name': _name, 'dob': _dob, 'address': _address, 'desc': _desc}})
		resp = jsonify('User updated successfully!')
		resp.status_code = 200
		return resp
	else:
		return not_found()
		
@app.route('/api/users/<id>', methods=['DELETE'])
def delete_user(id):
	mongo.db.users.delete_one({'_id': ObjectId(id)})
	resp = jsonify('User deleted successfully!')
	resp.status_code = 200
	return resp
		
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == "__main__":
    app.run()