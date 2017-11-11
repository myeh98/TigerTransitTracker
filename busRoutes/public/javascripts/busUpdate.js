processMoversUpdateRequest = (req, callback) =>
{
  if(req.readyState == 4 && req.status === 200) {
    res = JSON.parse(req.responseText)
    callback(res)
  }
}

getMoversUpdate = (callback) =>
{
  req = new XMLHttpRequest()
  req.onreadystatechange = () => processMoversUpdateRequest(req, callback)
  req.open('GET', '/movers/locations', true)
  req.send()
}
