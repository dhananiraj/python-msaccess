import pyodbc as pyo
print("init ...")

connection_string = (
	r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
	r"DBQ=E:\glory\msaccess-node\db.accdb"
	)
cnn = pyo.connect(connection_string)

import sys
from flask import Flask, jsonify, request
app = Flask(__name__)

def listToListOfDict(rows, keys):

	res = []

	# iterate over all the rows
	for row in rows:
		# index of the key
		index = 0

		# For JSON object
		dictionary = dict()

		for value in row:

			# Create a JSON Object
			dictionary[keys[index]] = value
			index += 1

		# add object to res array
		res.append(dictionary)

	return res

# Get all the category
@app.route('/category/all', methods=['GET'])
def get_all_data():
	try:
		cursor = cnn.cursor()
		qd = []
		# create a query for getting all the category
		query = f'''
					SELECT *
						FROM (
							SELECT Top 15
								*
								FROM
								(
									SELECT TOP 45
									*
									FROM category
									ORDER BY id
								) AS sub1
							ORDER BY sub1.id DESC
						) AS clients
					ORDER BY id
				'''
		cursor.execute(query)
		for row in cursor.fetchall():
			qd.append(tuple(row))
		cursor.close()
		return jsonify({'data': listToListOfDict(qd, ['id', 'categoryName']), 'message': 'Data Fetch Success', 'error': False}) , 200
	except Exception as e:
		return jsonify({'message': str(e), 'error': True}) , 500

# Get one category by id
@app.route('/category/<id>', methods=['GET'])
def get_one_data(id):
	try:
		cursor = cnn.cursor()
		qd = []
		# create a query for getting all the category
		query = f'select * from category where id = {id}'

		cursor.execute(query)
		for row in cursor.fetchall():
			qd.append(tuple(row))
		cursor.close()
		if len(qd) == 0:
			return jsonify({'message': 'Nothing found', 'error': False}) , 404


		return jsonify({'data': qd[0], 'message': 'Data Fetch Success', 'error': False}) , 200
	except Exception as e:
		return jsonify({'message': str(e), 'error': True}) , 500

# insert one category
@app.route('/category', methods=['POST'])
def insert_one_data():
	try:
		req = request.json # get the request data
		print(req, file=sys.stdout, flush=True)
		cursor = cnn.cursor()
		
		# create a query for inserting the category
		query = f"insert into category (categoryName) values ('{req['categoryName']}')"

		cursor.execute(query)
		cursor.commit()
		cursor.close()
		return jsonify({'message':'data inserted successfully!', 'error': False}) , 200
	except Exception as e:
		return jsonify({'message': str(e), 'error': True}) , 500

# update category
@app.route('/category/<id>', methods=['PUT'])
def update_one_data(id):
	try:
		req = request.json # get the request data
		print(req, file=sys.stdout, flush=True)
		cursor = cnn.cursor()
		
		# create a query for updating the category
		query = f"update category set categoryName='{req['categoryName']}' where id={id}"
		
		cursor.execute(query)
		cursor.commit()
		cursor.close()
		return jsonify({'message':'data updated successfully!', 'error': False}) , 200
	except Exception as e:
		return jsonify({'message': str(e), 'error': True}) , 500

# delete category
@app.route('/category/<id>', methods=['DELETE'])
def delete_one_data(id):
	try:
		cursor = cnn.cursor()
		
		# create a query for deleting the category
		query = f"delete from category where id={id}"
		
		cursor.execute(query)
		cursor.commit()
		cursor.close()
		return jsonify({'message':'data deleted successfully!', 'error': False}) , 200
	except Exception as e:
		return jsonify({'message': str(e), 'error': True}) , 500

if __name__ == '__main__':
	app.run(debug = True)
