let fst = eel.py_first_target()();
fst.then((res) => {
  target_lang = res[0];
  command = res[1];
  api_key = res[2];
  if (command == "ctrl+C") {
    document.querySelector("#cccc").checked = true;
  } else {
    document.querySelector("#ccandthen").checked = true;
    for (ccand of document.querySelectorAll("#ccand")) {
      ccand.disabled = !"disabled";
    }
  }
  var commandlist = command.split("+");
  for (ccand of document.querySelectorAll("#ccand")) {
    for (cmd of commandlist) {
      if (cmd == "ctrl" && ccand.name == "ctrl") {
        ccand.checked = true;
      } else if (cmd == "alt" && ccand.name == "alt") {
        ccand.checked = true;
      } else if (cmd == "shift" && ccand.name == "shift") {
        ccand.checked = true;
      }
    }
  }
  document.querySelector(".ccandlast").value =
    commandlist[commandlist.length - 1];

  console.log("first", target_lang + ":" + command + ":" + api_key + ":");
  document.querySelector("#target_lang").value = target_lang;
  document.querySelector("#deeplpro_apikey").value = api_key;
});

document.querySelector(".cancel_icon").addEventListener("click", (e) => {
  window.open("main.html", "_parent");
});
document.querySelector("#cccc").addEventListener("click", (e) => {
  for (ccand of document.querySelectorAll("#ccand")) {
    ccand.disabled = "disabled";
  }
});
document.querySelector("#ccandthen").addEventListener("change", (e) => {
  for (ccand of document.querySelectorAll("#ccand")) {
    ccand.disabled = !"disabled";
  }
});

function save() {
  var command = "";
  if (document.querySelector("#ccandthen").checked) {
    for (ccand of document.querySelectorAll("#ccand")) {
      if (ccand.type == "checkbox" && ccand.checked) {
        if (command == "") {
          command = ccand.name;
        } else {
          command += "+" + ccand.name;
        }
      } else if (ccand.type == "text") {
        if (ccand.value == "") {
          ccand.value = "C";
        }
        command += "+" + ccand.value;
      }
    }
    console.log(command);
  } else {
    command = "ctrl+C";
  }
  console.log(command, document.querySelector("#deeplpro_apikey").value);
  let save_settings = eel.py_save_settings(
    document.querySelector("#target_lang").value,
    command,
    document.querySelector("#deeplpro_apikey").value
  )();
  save_settings.then((res) => {
    console.log(res);
  });
}

document.querySelector("#save").addEventListener("click", (e) => {
  save();
});
document.querySelector(".ccandlast").addEventListener("input", (e) => {
  document.querySelector(".ccandlast").value = e.target.value.toUpperCase();
});
