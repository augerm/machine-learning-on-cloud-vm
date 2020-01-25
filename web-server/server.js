const http = require('http');
const WebSocket = require('ws');
const express = require('express');
const path = require('path');

const app = express();
const server = http.createServer(app);
const webSocketServer = new WebSocket.Server({ server });

const PORT = 8080;

const state = {
  query: null,
};

app.use(express.static('public'));
app.get('/', (req, res) => res.send(`Server running on port ${PORT}`));
app.get('/train', (req, res) => {
  state.query = req.query;
});
app.get('/status', (req, res) => {
  const responseText = "State: " + JSON.stringify(state);
  res.send(responseText);
  // res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

webSocketServer.on('connection', function connection(ws) {
  ws.on('message', function incoming(message) {
    console.log('received: %s', message);
  });

  ws.send('something');
});

server.listen(PORT);
console.log(`Listening on port ${PORT}`);