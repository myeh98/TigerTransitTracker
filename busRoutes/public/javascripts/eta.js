processPredictionRequest = (req, callback) =>
{
  if(req.readyState == 1) { predictionRequested(callback) }
  else if(req.readyState == 4) { predictionComplete(req,callback) }
}

predictionRequested = (callback) =>
{
  callback("Processing...")
}

predictionComplete = (req,callback) =>
{
  if (req.status !== 200){ 
    callback("Something went wrong")
  }
  else { 
    var res = JSON.parse(req.responseText)
    callback(res.eta)
  }
}

makePrediction = (lat, lon, callback) => 
{
  var params = {lat: lat, lon: lon} 
  var req = new XMLHttpRequest()

  req.onreadystatechange = () => processPredictionRequest(req, callback)
  req.open('POST', "/predict/eta", true)
  req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  req.send(JSON.stringify(params))
}
