let socket = io.connect(location.origin);

function setRelayOn(relay) {
    callApiWithRelay(relay, 'on');
}

function setRelayOff(relay) {
    callApiWithRelay(relay, 'off');
}

function toggleRelay(relay) {
    callApiWithRelay(relay, 'toggle');
}

function setRelayNotes(relay, notes) {
    callApiWithRelay(relay, 'notes', notes);
}

function setRelayName(relay, name) {
    callApiWithRelay(relay, 'name', name);
}

function setRelayDescription(relay, description) {
    callApiWithRelay(relay, 'description', description);
}

function setRelayInverted(relay, inverted) {
    callApiWithRelay(relay, 'inverted', inverted);
}

function callApiWithRelay(relay, command, data) {
    let url = relay + '/' + command;
    callApi(url, data);
}

function callApi(url, data) {
    console.log("Executing callApi", url, "with data: ", data);
    let type=(data !== undefined)?'POST':'GET'
    $.ajax({
      url: url,
      type: type,
      data: {"data": data},
    }).done(function () {
        console.log("Completed request");
    }).fail(function () {
        console.error("Relay status failure");
        Swal.fire({
            title: "Pi Relay Controller",
            text: "Server returned an error",
            type: "error"
        });
    });
}

function get_all_relay_status(callback) {
  console.log("Executing get_all_relay_status");
  $.get('all/status', function () {
      console.log("Sent request to server");
  }).done(function (res) {
    console.log(res);
    callback(JSON.parse(res));
  }).fail(function () {
      console.error("Relay status failure");
      Swal.fire({
          title: "Pi Relay Controller",
          text: "Server returned an error",
          type: "error"
      });
  });
}

function deleteRelayApi(relay) {
    console.log("Executing deleteRelayApi", relay);
    $.ajax({
      url: relay,
      type: 'DELETE'
    }).done(function () {
        console.log("Completed delete");
    }).fail(function () {
        console.error("Relay status failure");
        Swal.fire({
            title: "Pi Relay Controller",
            text: "Server returned an error",
            type: "error"
        });
    });
}

function addRelayApi(relay) {
    relayStr = JSON.stringify(relay)
    console.log("Executing addRelayApi: ", relayStr);
    $.ajax({
      url: '/',
      type: 'PUT',
      data: {"data": relayStr},
    }).done(function () {
        console.log("Completed addRelayApi");
        Swal.showValidationMessage(`Relay added sucesfully`);
    }).fail(function () {
        console.error("addRelayApi failure");
        Swal.showValidationMessage(`Error adding relay - check addresses`);
    });
}

function get_relay_types(callback) {
  console.log("Executing get_relay_types");
  $.get('types', function () {
      console.log("Sent request to server");
  }).done(function (res) {
      console.log(res);
      callback(JSON.parse(res));
  }).fail(function () {
      console.error("get_relay_types failure");
      Swal.fire({
          title: "Pi Relay Controller",
          text: "get_relay_types failure",
          type: "error"
      });
  });
}





function generateTable(relays) {
  console.log(relays);

  //Generate HEX string
  let hexCell = function(cell, formatterParams){ //plain text value
    return "0x"+cell.getValue().toString(16); //return the contents of the cell;
  };

  //Generate delete icon
  let deleteIcon = function(cell, formatterParams){ //plain text value
    return "<i class='fa fa-trash-o'></i>";
  };

  //Set status color
  let statusColor = function(cell, formatterParams){ //plain text value
    if (cell.getValue()) {
      //cell.getElement().style.backgroundColor = "green";
      //return "<i class='fa fa-toggle-on' style='color:#d33;'></i>";
      return "<i class='fa fa-toggle-on btn btn-success'></i>";
    } else {
      return "<i class='fa fa-toggle-off btn btn-danger'></i>";
    }
  };

  //Documentation at http://tabulator.info/docs/4.4/format
  let table = new Tabulator("#relays-table", {
      data:relays, //set initial table data
      persistenceMode: true,
      persistentLayout:true, //Enable column layout persistence
      persistentSort:true, //Enable sort persistence
      persistentFilter:true, //Enable filter persistence
      addRowPos:"bottom",
      columnVertAlign:"bottom", //align header contents to bottom of cell
      columns:[
        //Delete
        {formatter:deleteIcon, width:40, align:"center", headerSort:false, cellClick:function(e, cell){
          Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            type: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
          }).then((result) => {
            if (result.value) {
              let id = cell.getRow().getData().id;
              deleteRelayApi(id);
            }
          });
        }},
        //Name
        {title:"Name", field:"name", editor:"input", align:"center", cellEdited:function(cell){
          let id = cell.getRow().getData().id;
          setRelayName(id, JSON.stringify(cell.getValue()));
          }
        },
        //Status
        {title:"Status", field:"status", align:"center", formatter:statusColor, cellClick:function(e, cell){
            console.log(cell.getValue());
            let id = cell.getRow().getData().id;
            toggleRelay(id);
          }
        },
        {title:"ID", field:"id", align:"center",sorter:"number", formatter:hexCell},
        //Actions
        {
          title:"Addresses",
          columns:[
            {title:"Bus", field:"bus", align:"center", formatter:hexCell},
            {title:"Board", field:"board_address", align:"center", formatter:hexCell}
          ]
        },
        //Relay
        {
          title:"Relay",
          columns:[
            {title:"Number", field:"relay_number", align:"center"},
            {title:"Type", field:"typeName", align:"center"},
            //Inverted
            {title:"Inverted", field:"inverted", formatter:"tickCross", align:"center", cellClick:function(e, cell){
                let id = cell.getRow().getData().id;
                setRelayInverted(id, ! cell.getValue());
              }
            },
          ]
        },
        //Description
        {title:"Description", field:"description", editor:"input", cellEdited:function(cell){
          let id = cell.getRow().getData().id;
          setRelayDescription(id, JSON.stringify(cell.getValue()));
          }
        },
        //Notes
        {title:"Notes", field:"notes", editor:"input", width:400, cellEdited:function(cell){
          let id = cell.getRow().getData().id;
          setRelayNotes(id, JSON.stringify(cell.getValue()));
          }
        },
      ],
  });

  socket.on( 'connect', function() {
    console.log("CONECTED");
  });
  socket.on( 'updated_relays_status', function( relays ) {
    console.log( relays );
    table.setData(relays);
  })

}

//Add row on "Add Row" button click
$("#scan-button").click(function(){

  //Documentation at https://sweetalert2.github.io/#input-types
  Swal.fire({
    title: 'Scan I2C Bus',
    text: 'Select I2C Bus (1 by default) and press "Scan"',
    confirmButtonColor: '#3085d6',
    confirmButtonClass: 'btn btn-primary',
    confirmButtonText: 'Scan',
    showCancelButton: true,
    cancelButtonColor: '#d33',
    cancelButtonClass: 'btn btn-danger',
    cancelButtonText: 'Close',
    input: 'number',
    inputValue: 1,
    focusConfirm: false,
    width: 600,
    preConfirm: function(bus) {
      $.get('scan/'+bus, function () {
          console.log("Sent scan request to server");
      }).done(function (res) {
        console.log("Scan OK");
        console.log(res);
        scanResult = '<h3>Scan result</h3><pre><code>'+res+'</code></pre>';
          Swal.update({html:scanResult});
      }).fail(function () {
          console.error("Scan error");
          Swal.showValidationMessage(`Error scanning - valid bus?`);
      });
      return false
    }
  });
});


//Add row on "Add Row" button click
$("#add-button").click(function(){

  //Documentation at https://sweetalert2.github.io/#input-types
  Swal.fire({
    title: 'Adding Relays',
    confirmButtonColor: '#3085d6',
    confirmButtonClass: 'btn btn-primary',
    confirmButtonText: 'Add',
    showCancelButton: true,
    cancelButtonColor: '#d33',
    cancelButtonClass: 'btn btn-danger',
    cancelButtonText: 'Close',
    html:
      //Name
      '<h4>Name</h4>'+
      '<input id="swal-name" class="swal2-input" autofocus placeholder="My Relay">' +
      //Bus
      '<h4>Bus (Hex)</h4>'+
      '0x<input id="swal-bus" class="swal2-input" type="number" placeholder="1" pattern="[a-fA-F\d]+">' +
      //Board Address
      '<h4>Board Address (Hex)</h4>'+
      '0x<input id="swal-board_address" class="swal2-input" type="number" placeholder="10" pattern="[a-fA-F\d]+">' +
      //Relay Type
      '<h4>Relay Type</h4>'+
      '<select name=type id="swal-relay_type" class="swal2-input"></select>' +
      '<a id="swal-relay_type_desc"></a>' +
      //Relay Number
      '<h4>Relay Number (Hex)</h4>'+
      '0x<input id="swal-relay_number" class="swal2-input" type="number" placeholder="1" pattern="[a-fA-F\d]+">',
    onBeforeOpen: function() {
      let select = document.getElementById('swal-relay_type');
      let descDiv = document.getElementById('swal-relay_type_desc');
      get_relay_types(function(relay_types){
        //Insert types
        relay_types.forEach(function(value, index, array){
          let option = document.createElement("option");
          option.text = value.name;
          select.add(option, select.options[select.length]);
        })
        //Register for selection in order to update description
        function selectChange(){
          relay_types.forEach(function(value, index, array){
            if (select.value == value.name) {
              descDiv.textContent = value.description;
              descDiv.href = value.url;
            }
          });
        };
        select.onchange = selectChange;
        selectChange();
      });
    },
    preConfirm: function() {
      let name = document.getElementById('swal-name').value
      if (!name){
        Swal.showValidationMessage(`Name cannot be empty`);
        return false;
      }

      let bus = parseInt("0x" + document.getElementById('swal-bus').value);
      if (isNaN(bus)) {
        Swal.showValidationMessage(`Bus is not a valid number`);
        return false;
      }

      let board_address = parseInt("0x" + document.getElementById('swal-board_address').value);
      if (isNaN(board_address)) {
        Swal.showValidationMessage(`Board Address is not a valid number`);
        return false;
      }

      let relay_type = parseInt("0x" + document.getElementById('swal-relay_type').value);
      if (isNaN(relay_type)) {
        Swal.showValidationMessage(`Relay Type is not a valid number`);
        return false;
      }

      let relay_number = parseInt("0x" + document.getElementById('swal-relay_number').value);
      if (isNaN(relay_number)) {
        Swal.showValidationMessage(`Relay Number is not a valid number`);
        return false;
      }

      addRelayApi({
            type: relay_type,
            name: name,
            bus: bus,
            board_address: board_address,
            relay_number: relay_number
          });
      return false;
    }
  });
});

$("#all-on").click(function(){
    setRelayOn('all');
});
$("#all-off").click(function(){
    setRelayOff('all');
});
$("#all-toggle").click(function(){
    toggleRelay('all');
});

//Generate table
get_all_relay_status(generateTable);
