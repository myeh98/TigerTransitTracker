var express = require('express')
var router = express.Router();
var predictEta = require('./etaPredictor')

router.get('/', (req, res) =>
{
  res.render('../client/views/pages/index')
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

