const express = require('express')
const app = express()
const port = 3000

const router = require('./server/router')
const bodyParser = require('body-parser')

app.use(bodyParser.urlencoded({ extended: true }))
app.use(bodyParser.json())

app.set('view engine', 'ejs');  

app.use(express.static('public'))
app.use('/', router)

app.listen(port, () =>
  console.log(`Listening on port ${port}`)
)
