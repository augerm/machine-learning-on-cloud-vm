// const ws = new WebSocket('ws://localhost:8080');

// ws.onopen = () => {
//     alert("Connected successfully");
//     ws.send('hello server');
// }
const fileUploadEl = document.getElementById('csv-file');
const uploadBtnEl = document.getElementById('upload-btn');

uploadBtnEl.addEventListener('click', () => {
    const file = fileUploadEl.files[0];
    // TODO: Upload file
});