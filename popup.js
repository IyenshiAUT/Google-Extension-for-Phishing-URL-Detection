const featureInput = document.getElementById("featureInput");
const result = document.getElementById("result");

function removeHttp(url) {
  // Use a regular expression to remove "http://" or "https://"
  return url.replace(/^https?:\/\//, '');
}


async function checkUrl() {

  const urlContent = featureInput.value.trim();
  // Simulate error prediction (replace this with real prediction logic)
  if (urlContent === "") {
    // error message when url is not provided and clicked
    const errorMessage = "Please provide a URL, first !";
    result.innerText = errorMessage;
  } else {
    // prepare the error message for prediction
    const urlContent = featureInput.value.trim();
    urlContentRemovedHttp = removeHttp(urlContent)
    featureInput.value = '';
    // send the request to get the prediction
    try {
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ data: urlContentRemovedHttp})
      });
      const data = await response.json();
      prediction = data['prediction']
      if (prediction == 0){
        // when url is safe
        result.innerText = "This URL is safe!";
      }
      else{
        // when url is phishing
        result.innerText = "Warning: Phishing URL detected!"
      }
    } catch {
      // when an error
      result.innerText = "Error in fetching prediction";
    }
  }
}

// Event listener for prediction on button click
document.getElementById("submit-button").addEventListener("click", (e) => {
  e.preventDefault();
  checkUrl();
});




