const fs = require('fs')
fs.writeFileSync('./.env', `GoogleMapsKey=${process.env.GoogleMapsKey}\n`)