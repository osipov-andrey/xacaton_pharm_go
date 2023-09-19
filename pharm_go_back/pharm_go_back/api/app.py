from quart import Quart, request, render_template, jsonify
from motor.motor_asyncio import AsyncIOMotorClient
import json
from pymongo import MongoClient

app = Quart(__name__)

# MongoDB configuration
MONGO_URI = "mongodb://localhost:27017"

async def save_medication(data):
    print('data =', data)
    try:
        async with AsyncIOMotorClient(MONGO_URI) as client:
            db = client.medicine_database
            collection = db.medicines

            # Ensure that data is valid JSON
            try:
                data = json.loads(data)
            except json.JSONDecodeError as json_error:
                raise ValueError(f"Invalid JSON data: {str(json_error)}")

            # Insert the JSON data into the "medicines" collection
            result = await collection.insert_one(data)
            
            if result.inserted_id:
                return 'Medication JSON saved successfully.', 200
            else:
                return 'Failed to save medication JSON.', 500

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error while saving medication JSON: {str(e)}")
        return 'Failed to save medication JSON.', 500


@app.route('/')
async def index():
    return await render_template('index.html')

@app.route('/search', methods=['POST'])
async def search_medicine():
    try:
        # Get the search query from the form
        search_query = (await request.form)['query']

        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        db = client['medicine_database']

        # Query MongoDB to find medicines with a name that matches the search query
        results = db.medicines.find(
            {'name': {'$regex': search_query, '$options': 'i'}},
            {'_id': 0, 'name': 1, 'pharmacy': 1, 'price': 1}
        )

        # Convert the MongoDB cursor to a list of dictionaries
        medicine_list = list(results)

        # Close the MongoDB connection
        client.close()

        # Prepare the JSON response
        return jsonify(medicine_list), 200

    except Exception as e:
        return str(e), 500


@app.route('/save', methods=['POST'])
async def save_medication_route():
    try:
        data_bytes = await request.data

        # Convert the bytes to a JSON string
        data_string = data_bytes.decode('utf-8')

        # Parse the JSON data
        data = json.loads(data_string)

        #data = await request.get_data()
        print('data =', data)
        print('datatype =', type(data))
        for item in data:
            # Ensure that data is valid JSON
            #try:
            #    data_json = json.loads(item.decode('utf-8'))
            #except json.JSONDecodeError as json_error:
            #    raise ValueError(f"Invalid JSON data: {str(json_error)}")
            print(type(item))
            print(item)
            # Connect to MongoDB using PyMongo
            client = MongoClient(MONGO_URI)
            db = client['medicine_database']
            collection = db['medicines']
        
            # Insert the JSON data into the "medicines" collection
            result = collection.insert_one(item)
            print(result)
            client.close()

            if result.inserted_id:
                return 'Medication JSON saved successfully.', 200
            else:
                return 'Failed to save medication JSON.', 500

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error while saving medication JSON: {str(e)}")
        return 'Failed to save medication JSON.', 500
    
if __name__ == '__main__':
    app.run()
