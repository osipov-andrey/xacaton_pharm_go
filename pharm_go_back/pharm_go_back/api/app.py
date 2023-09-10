from quart import Quart, request, jsonify  # Use 'quart.jsonify' for Quart
import json
import subprocess

app = Quart(__name__)

@app.route("/search", methods=["POST", "GET"])
async def search_medicine():
    try:
        form_data = await request.form
        search_query = form_data.get("query")
        print('search_query =', search_query)

        # Execute external_script.py to search for medicine
        script_output = subprocess.check_output(["python3", "external_script.py", search_query])
        search_results = json.loads(script_output.decode())  # Use 'decode()' to convert bytes to a string
        print(search_results)
        # Use 'quart.jsonify' to return JSON response
        return jsonify(search_results)
    except Exception as e:
        print("error", str(e))
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
