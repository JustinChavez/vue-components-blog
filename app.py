from flask import Flask, render_template, request
import requests

app = Flask(__name__)

'''Backend'''
# Called by Vue to retrieve the properties of each PDB from KLIFS
@app.route('/pdb_id/<pdb_id>', methods=['GET'])
def klifs_pdb_data(pdb_id):
    # API Endpoint
    URL = "https://klifs.net/api/structures_pdb_list"
    
    # PDB we would like to query for
    PARAMS = {'pdb-codes': pdb_id}

    # Send the GET request to the API and retrieve any returned data
    res = requests.get(url = URL, params = PARAMS)
    data = res.json()

    # If an error occured, return the error
    if res.status_code == 400:
        return data[1], 400
        
    # Return the first set of PDB characteristics
    return data[0]

'''Frontend'''
# Loads Vue component that renders the KLIFS selector
@app.route("/frontend/")
def vue_selector():
    return render_template('frontend.html')

# Embeds Vue component into a post form
@app.route("/flask_form/", methods = ['POST', 'GET'])
def vue_post():
    if request.method == 'GET':
        return render_template("flask_form.html")

    elif request.method == 'POST':
        task_name = request.form.get("task_name")
        # Grab values from Vue Component
        dfg = request.form.get("dfg")
        ac_helix = request.form.get("ac_helix")

        # Compute feature vector and display it as a Python List
        # feature_vector = one_hot_protein_features(dfg, ac_helix).numpy().tolist()
        return render_template("flask_form.html", task_name=task_name, dfg=dfg, ac_helix=ac_helix)