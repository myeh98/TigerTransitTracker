var express = require('express')
var router = express.Router();
var predictEta = require('./etaPredictor')
var busUpdate = require('./busUpdater')

router.get('/', (req, res) =>
{
  res.render('../client/views/pages/index')
})

router.get('/movers/locations', (req, res) =>
{
  newLocs = busUpdate()
  res.json(newLocs)
  console.log('Bus update sent ' + JSON.stringify(newLocs))
})

router.post('/predict/eta', (req, res) => 
{
  var lat = req.body.lat
  var lon = req.body.lon
  predictEta(lat, lon, (eta) => 
  {
    res.json({eta: eta})
  })
  console.log("Predicting for " + lat + " " + lon)
})

module.exports = router

