const ws = new WebSocket('ws://localhost:8080');

ws.onopen = () => {
    alert("Connected successfully");
    ws.send('hello server');
}