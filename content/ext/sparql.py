import requests
import pandas as pd
from IPython.display import HTML
import urllib3

# Suppress the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def query(query_string, store="L"):
    """
    Sends a SPARQL query to a SPARQL endpoint and returns the results as a pandas DataFrame.
    
    Parameters:
    - query_string: The SPARQL query string.
    - store: The URL of the SPARQL endpoint (triple store) or some predefined abbrevations.
    
    Returns:
    - A pandas DataFrame containing the query results.
    """
    # Define the headers for the request
    headers = {
        'Accept': 'application/sparql-results+json',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    # three Swiss triplestores
    if store == "F":
        address = 'https://fedlex.data.admin.ch/sparqlendpoint'
    elif store == "G":
        address = 'https://geo.ld.admin.ch/query'
    elif store == "L":
        address = 'https://ld.admin.ch/query'
    else:
        address = store

    # URL-encode the query parameters
    payload = {'query': query_string}
    
    # Send the request to the SPARQL endpoint
    response = requests.post(address, data=payload, headers=headers)

    # Ensure the response uses UTF-8 encoding
    response.encoding = 'utf-8'
    
    # Raise an exception if the request was not successful
    response.raise_for_status()
    
    # Parse the JSON response
    results = response.json()
    
    # Extract the variable names and the data
    columns = results['head']['vars']
    data = [
        {var: binding.get(var, {}).get('value') for var in columns}
        for binding in results['results']['bindings']
    ]
    
    # Create a pandas DataFrame from the data
    df = pd.DataFrame(data, columns=columns)

    # Convert columns to numeric datatype if possible
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')
    
    return df

def display_result(df):
    df = HTML(df.to_html(render_links=True, escape=False))
    display(df)
