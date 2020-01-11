const http = require('http');
const WebSocket = require('ws');
const express = require('express');

const app = express();
const server = http.createServer(app);
const webSocketServer = new WebSocket.Server({ server });

const PORT = 8080;

app.use(express.static('public'))
app.get('/', (req, res) => res.send('Hello World!'))

webSocketServer.on('connection', function connection(ws) {
  ws.on('message', function incoming(message) {
    console.log('received: %s', message);
  });

  ws.send('something');
});

server.listen(PORT);
console.log(`Listening on port ${PORT}`);