const http = require('http');
const WebSocket = require('ws');
const express = require('express');
const path = require('path');
const {spawn} = require("child_process");

const app = express();
const server = http.createServer(app);
const webSocketServer = new WebSocket.Server({ server });

const PORT = 8080;

const state = {
  query: null,
};

app.use(express.static('public'));
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html')).statusCode(200);
});
app.get('/train', (req, res) => {
  console.log("Got request", req.query.data);
  state.query = req.query;
  const pythonScript = path.join(__dirname, '../', 'NeuralNet', 'main.py');
  const outDir = path.join(__dirname, 'data');
  const pythonProcess = spawn('python3', [pythonScript, `--csv=${req.query.data}`, `--out_dir=${outDir}`]);
  pythonProcess.stdout.on('data', (data) => {
    console.log(`child stdout:\n${data}`);
  });
  pythonProcess.stderr.on('data', (data) => {
    console.error(`child stderr:\n${data}`);
  });
  res.send("Training started successfully.").statusCode(200);
});
app.get('/status', (req, res) => {
  const responseText = "State: " + JSON.stringify(state);
  res.send(responseText).statusCode(200);
});

webSocketServer.on('connection', function connection(ws) {
  ws.on('message', function incoming(message) {
    console.log('received: %s', message);
  });

  ws.send('something');
});

server.listen(PORT);
console.log(`Listening on port ${PORT}`);