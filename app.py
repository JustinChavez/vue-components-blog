from flask import Flask, render_template, request
import requests
import tensorflow as tf

DFG_CONFORMATION = ["in", "out", "out-like"]
AC_CONFORMATION = ["in", "out", "na"]

app = Flask(__name__)

'''Frontend'''
# Loads Vue component that renders the KLIFS selector
@app.route("/frontend/")
def vue_selector_example():
    return render_template('frontend.html')

# Embeds Vue component into a post form
@app.route("/flask_form/", methods = ['POST', 'GET'])
def vue_post_example():
    if request.method == 'GET':
        return render_template("flask_form.html")

    elif request.method == 'POST':
        job_name = request.form.get("jobName")
        # Grab values from Vue Component
        dfg = request.form.get("dfg")
        ac_helix = request.form.get("ac_helix")

        # Compute feature vector and display it as a Python List
        feature_vector = one_hot_protein_features(dfg, ac_helix).numpy().tolist()
        return render_template("success.html", job_name=job_name, dfg=dfg, ac_helix=ac_helix, feature_vector=feature_vector)

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

def one_hot_protein_features(dfg, alpha_c):
    
    #one-hot encoding of dfg conformation
    dfg_idx = DFG_CONFORMATION.index(dfg)
    dfg_one_hot = tf.one_hot(dfg_idx, len(DFG_CONFORMATION))
    
    #one-hot encoding of alpha c helix conformation
    alpha_c_idx = AC_CONFORMATION.index(alpha_c)
    alpha_c_one_hot = tf.one_hot(alpha_c_idx, len(AC_CONFORMATION))
    
    #combine the two one-hot encodings into a single feature vector
    return tf.concat([dfg_one_hot, alpha_c_one_hot], 0)
