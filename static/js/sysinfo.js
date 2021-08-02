var data = {
    labels: [],
    datasets: [{
      label: "CPU usage %",
      fill: true,
      lineTension: 0.1,
      backgroundColor: "rgba(0,255,0,0.4)",
      borderColor: "green", // The main line color
      borderCapStyle: 'square',
      pointBorderColor: "white",
      pointBackgroundColor: "green",
      pointBorderWidth: 1,
      pointHoverRadius: 8,
      pointHoverBackgroundColor: "yellow",
      pointHoverBorderColor: "green",
      pointHoverBorderWidth: 2,
      pointRadius: 4,
      pointHitRadius: 10,
      data: [],
      spanGaps: true,
    }]
  };
  const config = {
    type: 'line',
    data: data,
    options: {}
  };
  var chart = new Chart(
    document.getElementById('myChart'),
    config
  );
  
  function addData(chart, label, data) {
      chart.data.labels.push(label);
      chart.data.datasets.forEach((dataset) => {
          dataset.data.push(data);
      });
      chart.update();
  }

  let timerId = setInterval(() => {
    updateCPU();
  }, 2000);

  function updateCPU(){
    let json = JSON.stringify({
      method: "getcpu"
    });

    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/api');
    xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    xhr.send(json);
    xhr.onload = function () {
        addData(chart, xhr.response.split('|')[1], xhr.response.split('|')[0])
      
    }
  }