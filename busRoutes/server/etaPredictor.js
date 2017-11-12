var pythonShell = require('python-shell')
var BusLocations = require('./busUpdater')

predict = ((locationName, callback) => {
  args = []
  busData = BusLocations()

  args.push(locationName)
  console.log("aou" + busData)
  busData.forEach( (bus) => {
    args.push(bus.bus)
    args.push(bus.rt)
    args.push(bus.prevDest)
    args.push(bus.distNext)
    args.push(bus.tPrev)
  })
  console.log(args)
  var options = {
    scriptPath: 'server/python/',
    args: busData 
  }
  pythonShell.run('etaPredictor.py', 
                  options, 
                  (err,results) => 
  {
    if (err) throw err
    callback(results)
  })
})

module.exports = predict
