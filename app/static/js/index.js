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

function callApiWithRelay(relay, command, data) {
    let url = relay + '/' + command;
    callApi(url, data);
}

function callApi(url, data) {
    console.log("Executing callApi", url);
    let type=data?'POST':'GET'
    $.ajax({
      url: url,
      type: type,
      data: {"data": data},
    }).done(function () {
        console.log("Completed request");
    }).fail(function () {
        console.error("Relay status failure");
        swal({
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
      console.log("Completed request");
      callback(JSON.parse(res));
  }).fail(function () {
      console.error("Relay status failure");
      swal({
          title: "Pi Relay Controller",
          text: "Server returned an error",
          type: "error"
      });
  });
}

function generateRow(table, relay, index) {
  let row, th, cell, group, text, btn;

  row = table.insertRow();

  //Row Header
  th = document.createElement("th");
  th.style.textAlign = "center";
  th.style.verticalAlign = "middle";
  th.setAttribute('scope', 'row');
  if (index == '"all"') {
    text = document.createTextNode(relay.name);
  } else {
    text = document.createElement("INPUT");
    text.setAttribute("type", "text");
    text.style.textAlign = "center";
    text.style.width = "100%";
    text.value = relay.name;
    text.setAttribute('onchange', `
      console.log(this.value);
      setRelayName(`+index+`, this.value);
    `);
  }
  th.appendChild(text);
  row.appendChild(th);

  //Status
  cell = row.insertCell();
  cell.setAttribute('id', 'status_'+index);
  cell.style.textAlign = "center";
  cell.style.verticalAlign = "middle";
  if (index != '"all"') cell.style.backgroundColor = relay.status?'green':'red';
  text = document.createTextNode(relay.status?'ON':'OFF');
  if (index != '"all"') cell.appendChild(text);

  //Buttons group
  cell = row.insertCell();
  cell.style.textAlign = "center";
  cell.style.verticalAlign = "middle";
  group = document.createElement('DIV');
  group.setAttribute('class', 'btn-group-lg');
  group.setAttribute('role', 'group');
  group.setAttribute('aria-label', relay.name);
  cell.appendChild(group);

  //On
  btn = document.createElement('BUTTON');
  btn.innerHTML = 'On';
  btn.setAttribute('onclick', 'setRelayOn('+index+');');
  btn.setAttribute('type', 'button');
  btn.setAttribute('class', 'btn btn-success');
  group.appendChild(btn);

  //Off
  btn = document.createElement('BUTTON');
  btn.innerHTML = 'Off';
  btn.setAttribute('onclick', 'setRelayOff('+index+');');
  btn.setAttribute('type', 'button');
  btn.setAttribute('class', 'btn btn-danger');
  group.appendChild(btn);

  //Toggle
  btn = document.createElement('BUTTON');
  btn.innerHTML = 'Toggle';
  btn.setAttribute('onclick', 'toggleRelay('+index+');');
  btn.setAttribute('type', 'button');
  btn.setAttribute('class', 'btn btn-info');
  group.appendChild(btn);

  //Notes
  cell = row.insertCell();
  cell.style.textAlign = "center";
  cell.style.verticalAlign = "middle";
  text = document.createElement("TEXTAREA");
  text.setAttribute('id', 'text_'+index);
  text.setAttribute("type", "text");
  text.style.textAlign = "center";
  text.style.width = "100%";
  text.value = relay.notes;
  text.setAttribute('onchange', `
    console.log(this.value);
    setRelayNotes(`+index+`, this.value);
  `);
  if (index != '"all"') cell.appendChild(text);
}

function generateTable(relays) {
  console.log(relays);
  let table = document.querySelector("table");

  relays.forEach( function (relay, index) {
    generateRow(table, relay, index);
  });

  generateRow(table, {'name':'ALL','description':'','status':'','notes':''}, '"all"');

  //Header
  let thead, row, text;

  thead = table.createTHead();
  row = thead.insertRow();

  //Relay
  th = document.createElement("th");
  th.style.textAlign = "center";
  text = document.createTextNode('Name');
  th.appendChild(text);
  row.appendChild(th);

  //Status
  th = document.createElement("th");
  th.style.textAlign = "center";
  text = document.createTextNode('Status');
  th.appendChild(text);
  row.appendChild(th);

  //Actions
  th = document.createElement("th");
  th.style.textAlign = "center";
  text = document.createTextNode('Actions');
  th.appendChild(text);
  row.appendChild(th);

  //Notes
  th = document.createElement("th");
  th.style.textAlign = "center";
  text = document.createTextNode('Notes');
  th.appendChild(text);
  row.appendChild(th);
}

//Generate table
get_all_relay_status(generateTable);

socket.on( 'connect', function() {
  console.log("CONECTED");
});
socket.on( 'updated_relays_status', function( relays ) {
  console.log( relays )
  relays.forEach( function (relay, index) {
  let cell = document.getElementById('status_'+index);
  if (relay.status) {
    cell.style.backgroundColor = 'green';
    cell.innerHTML = 'ON';
  } else {
    cell.style.backgroundColor = 'red';
    cell.innerHTML = 'OFF';
  }
  });
})
