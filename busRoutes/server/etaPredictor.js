var pythonShell = require('python-shell')
var BusLocations = require('./busUpdater')

predict = ((locationName, callback) => {
  args = []
  busData = BusLocations()

  args.push(locationName)
  busData.forEach( (bus) => {
    args.push(bus.pos.lat)
    args.push(bus.pos.lng)
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
