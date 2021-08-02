
        document.querySelectorAll('.viewLog').forEach(element => {
        
            element.addEventListener("click", (event) => {
                let json = JSON.stringify({
                    method: "getlog",
                    dir: event.target.dataset.fold
                });
                let xhr = new XMLHttpRequest();
                xhr.open('POST', '/api');
                xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
                xhr.send(json);
                xhr.onload = function () {
                if (xhr.status != 200) {
                    alert(`Error ${xhr.status}: ${xhr.statusText}`);
                } else {
                    document.querySelector('.modal-body').innerHTML = '';
                    mw = xhr.response.split('\n');
                    mw.forEach(el => {
                        a  = document.createElement( "p" );
                        a.innerText = el;
                        document.querySelector('.modal-body').append(a);
                    })
                    $('#exampleModal').modal('show')
                }
                };
            });
        });


    