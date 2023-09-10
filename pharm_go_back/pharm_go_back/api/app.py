import punq
from quart import Quart, request, jsonify  # Use 'quart.jsonify' for Quart
import json
import subprocess

from repository.interface import Med, MedsRepoProto
from repository.local_repo import MedsRepoLocal

app = Quart(__name__)


@app.route("/med", methods=["POST"])
async def save_med():
    repo: MedsRepoProto = container.resolve(MedsRepoProto)
    body = await request.get_data()
    meds = [Med(**med) for med in json.loads(body)]
    print(meds)
    for med in meds:
        await repo.save_med(med)
    return f"{len(meds)} meds have been saved", 201


@app.route("/med", methods=["GET"])
async def get_meds() -> dict:
    repo: MedsRepoProto = container.resolve(MedsRepoProto)
    return await repo.get_meds()


@app.route("/med/<name>", methods=["GET"])
async def get_med(name: str) -> dict:
    repo: MedsRepoProto = container.resolve(MedsRepoProto)
    med_info = await repo.get_med(name)
    return med_info.model_dump()


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
    container = punq.Container()
    container.register(MedsRepoProto, instance=MedsRepoLocal())
    app.config["container"] = container

    app.run(host="0.0.0.0", port=5005, debug=True)
