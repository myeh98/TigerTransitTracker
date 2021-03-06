var PythonShell = require('python-shell')

var busData = []

var busLocOptions = {
  scriptPath: 'server/python/',
  pythonPath: '/usr/bin/python3.5',
  mode: 'json'
}
shell = new PythonShell('busLocation.py', busLocOptions)

shell.on('message', function (message) {
  busData = message;
});

shell.end(function (err) {
  if (err) throw err;
  console.log('finished');
});

busUpdate = () =>
{
  return busData 
}

module.exports = busUpdate
