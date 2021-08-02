//infoBTN
function updateTable(b){
    let json = JSON.stringify({
      method: "get"
    });

    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/api');
    xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    xhr.send(json);
    xhr.onload = function () {
      if (xhr.status != 200) {
        alert(`Error ${xhr.status}: ${xhr.statusText}`);
      } else {
        if (xhr.response != "No projs"){

        
        //var jser = JSON.parse(xhr.response);
        if (xhr.response.includes("||")){
          b.clear().draw();
          ab = xhr.response.split('||');
          ab.forEach((item) => {
            if (item != ""){
              b.row.add( [
                item.split(' | ')[0],
                '<p class="text-success">' + item.split(' | ')[1] + '</p>',
                item.split(' | ')[2],
                item.split(' | ')[3],
                item.split(' | ')[4],
                item.split(' | ')[5],
                item.split(' | ')[6],
                item.split(' | ')[9],
                item.split(' | ')[8],
                item.split(' | ')[7],
                '<button class="btn btn-danger stopBtn" data-proc="'+item.split(' | ')[10]+'">STOP</button>'
              ] ).draw( false );
              updateStopBtn();
            }
           
          });
        }else {
          b.clear().draw();
          b.row.add( [
              xhr.response.split(' | ')[0],
              xhr.response.split(' | ')[1],
              xhr.response.split(' | ')[2],
              xhr.response.split(' | ')[3],
              xhr.response.split(' | ')[4],
              xhr.response.split(' | ')[5],
              xhr.response.split(' | ')[6],
              xhr.response.split(' | ')[9],
              xhr.response.split(' | ')[8],
              xhr.response.split(' | ')[7],
              '<button class="btn btn-danger stopBtn" data-proc="'+xhr.response.split(' | ')[10]+'">STOP</button>'
          ] ).draw( false );
          updateStopBtn();
        }
      }else {
        b.clear().draw();
      }
      }
    };
  }
  
  function updateStopBtn(){
    //STOPBTN
    document.querySelectorAll('.stopBtn').forEach(element => {
      
      element.addEventListener("click", (event) => {
          let json = JSON.stringify({
            method: "stop",
            id: event.target.dataset.proc
          });

          let xhr = new XMLHttpRequest();
          xhr.open('POST', '/api');
          xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
          xhr.send(json);
          xhr.onload = function () {
            if (xhr.status != 200) {
              alert(`Error ${xhr.status}: ${xhr.statusText}`);
            } else {
              document.location.reload();
            }
          };
      });
    });
  }
  
  $(document).ready( function () {
    var t = $('#table_id').DataTable({
      "searching": false,
      paging: false,
      responsive: true
    });
    let timerId = setInterval(() => {
      updateTable(t);
      
    }, 500);
    
} );

  