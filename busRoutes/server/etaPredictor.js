var pythonShell = require('python-shell')

predict = (lat, lon, callback) =>
{

  var options = {
    scriptPath: 'server/python/',
    args: [lat,lon]
  }
  pythonShell.run('etaPredictor.py', 
                  options, 
                  (err,results) => 
  {
    if (err) throw err
    callback(results)
  })
}

module.exports = predict
