from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import numpy as np
from flask_cors import CORS
from functions import (
    url_length,
    is_ip_address,
    calculate_entropy,
    dot_count,
    at_count,
    dash_count,
    has_punycode,
    digit_letter_ratio,
    contains_tld_in_subdirectory,
    domain_has_digits,
    subdomain_count,
    calculate_char_entropy,
    has_internal_links
)


app = Flask(__name__)
CORS(app)


with open('phishing_url_detection_model.pkl', 'rb') as f:
    model = pickle.load(f)


@app.route('/predict', methods=['POST'])
def predict():
    # Get JSON data from the POST request
    data = request.get_json()
    print(data)

    # Check if the data is None or doesn't have 'text' key
    if data is None or "data" not in data:
        return jsonify({'error': 'No URL provided or invalid input.'}), 400

    # Retrieve URL from JSON data
    url = data['data']
    print(url)
    

    # Feature extraction from URL
    urlLength = url_length(url)
    
    isIpAddress = is_ip_address(url)
    print(isIpAddress, "Hello")
    calculateEntropy = calculate_entropy(url)
    print(calculateEntropy)
    dotCount = dot_count(url)
    print(dotCount)
    atCount = at_count(url)
    print(atCount)
    dashCount = dash_count(url)
    print(dashCount)
    hasPunyCode = has_punycode(url)
    print(hasPunyCode)
    digitLetterRatio = digit_letter_ratio(url)
    print(digitLetterRatio)
    containsTId = contains_tld_in_subdirectory(url)
    print(containsTId)
    domainHasDigits = domain_has_digits(url)
    print(domainHasDigits)
    subdomainCount = subdomain_count(url)
    print(subdomainCount)
    calculateCharEntropy = calculate_char_entropy(url)
    print(calculateCharEntropy)
    hasInternalLinks = has_internal_links(url)
    print(hasInternalLinks)
    
    data_to_predict = {
        'url_length': [urlLength],
        'starts_with_ip': [isIpAddress],
        'url_entropy': [calculateEntropy],
        'has_punycode': [hasPunyCode],
        'digit_letter_ratio': [digitLetterRatio],
        'dot_count': [dotCount],
        'at_count': [atCount],
        'dash_count': [dashCount],
        'tld_count': [containsTId],
        'domain_has_digits': [domainHasDigits],
        'subdomain_count': [subdomainCount],
        'nan_char_entropy': [calculateCharEntropy],
        'has_internal_links': [hasInternalLinks],
    }
    # Convert the dictionary to a DataFrame
    df_to_predict = pd.DataFrame(data_to_predict)
    print(df_to_predict)

    # Make predictions using the loaded model
    predictions = model.predict(df_to_predict)


    return jsonify({'prediction': int(predictions[0])})


if __name__ == '__main__':
    app.run(debug=True)
