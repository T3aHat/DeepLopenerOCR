let fst = eel.py_get_settings()();
let target_lang;
let command;
let api_key;
let freeFlag;
//ocrFlagはmainでのみ編集可とする
let ocrFlag;
fst.then((res) => {
  target_lang = res[0];
  command = res[1];
  api_key = res[2];
  freeFlag = res[3];
  ocrFlag = res[4];
  document.querySelector("#freeFlag").value = freeFlag;
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
  document.querySelector("#target_lang").value = target_lang;
  document.querySelector("#deepl_apikey").value = api_key;
  document.querySelector("#save").addEventListener("click", (e) => {
    if (document.querySelector("#deepl_apikey").value == "") {
      document.querySelector(".save_message").textContent = "Enter API_KRY";
      setTimeout(function () {
        document.querySelector(".save_message").textContent = "";
      }, 2000);
    } else {
      save();
      document.querySelector(".save_message").textContent = "saved";
      setTimeout(function () {
        eel.py_open_options()();
        window.open("main.html", "_parent");
      }, 2000);
    }
  });
  document.querySelector(".ccandlast").addEventListener("input", (e) => {
    document.querySelector(".ccandlast").value = e.target.value.toUpperCase();
  });

  document.querySelector(".back_icon").addEventListener("click", (e) => {
    eel.py_open_options()();
    window.open("main.html", "_parent");
  });

  if (document.querySelector("#deepl_apikey").value == "") {
    document.querySelector("#deepl_apikey").style.border = "2px solid red";
    document.querySelector(".required").textContent = "Enter DeepL API_KEY";
  }
  document.querySelector("#deepl_apikey").addEventListener("input", (e) => {
    if (document.querySelector("#deepl_apikey").value == "") {
      document.querySelector("#deepl_apikey").style.border = "2px solid red";
      document.querySelector(".required").textContent = "Enter DeepL API_KEY";
    } else {
      document.querySelector("#deepl_apikey").style.border = "";
      document.querySelector(".required").textContent = "";
    }
  });
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
  } else {
    command = "ctrl+C";
  }
  let save_settings = eel.py_save_settings(
    document.querySelector("#target_lang").value,
    command,
    document.querySelector("#deepl_apikey").value,
    document.querySelector("#freeFlag").value,
    ocrFlag
  )();
  save_settings.then((res) => {});
}
