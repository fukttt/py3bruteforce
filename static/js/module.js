document.getElementById('startBtn').addEventListener("click", () => {
    document.querySelector('.load').style.display = "block";
    let json = JSON.stringify({
        method: "start",
        module: modul,
        base: 'sources/' + document.getElementById('baseName').value,
        proxy: 'sources/' + document.getElementById('proxyName').value,
        proxytype: document.getElementById('proxyType').value,
        threads: document.getElementById('threadsCount').value,
        timeout: document.getElementById('timeOut').value,
        proxylink: document.getElementById('prl').value,
    });

    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/api');
    xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    xhr.send(json);
    xhr.onload = function () {
        if (xhr.status != 200) {
            alert(`Error ${xhr.status}: ${xhr.statusText}`);
        } else {
            document.location = "/";
        }
    };
}, false);
document.getElementById('debugBtn').addEventListener("click", () => {
    alert('Will be soon');
}, false);