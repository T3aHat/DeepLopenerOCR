let target_lang;
let command;
let api_key;
let freeFlag;
let ocrFlag;
let fst = eel.py_get_settings()();
fst.then((res) => {
  target_lang = res[0];
  command = res[1];
  api_key = res[2];
  freeFlag = res[3];
  ocrFlag = res[4];
  if (res[5]) {
    //first open
    window.close();
  } else {
    document.querySelector("#target_lang").value = target_lang;
    if (ocrFlag == "True") {
      document.querySelector("#ocr_btn").checked = true;
    } else {
      document.querySelector("#ocr_btn").checked = false;
    }
    if (api_key == "") {
      eel.py_open_options()();
      window.open("options.html", "_parent");
    }
    eel.expose(js_translate);
    function js_translate(clipboard, target_lang, api_key) {
      document.querySelector(".translator_source_textarea").value = clipboard;
      document.querySelector("#target_lang").value = target_lang;
      api_translate(clipboard, target_lang, api_key);
    }
  }

  function api_translate(txt, target_lang, api_key) {
    document.querySelector(".message").textContent = "translating...";
    let api_url;
    if (freeFlag == "Free") {
      api_url = "https://api-free.deepl.com/v2/translate";
    } else {
      api_url = "https://api.deepl.com/v2/translate";
    }
    var params = {
      auth_key: api_key,
      text: txt,
      target_lang: target_lang,
    };
    var data = new URLSearchParams();
    Object.keys(params).forEach((key) => data.append(key, params[key]));
    fetch(api_url, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; utf-8",
      },
      body: data,
    }).then((res) => {
      document.querySelector(".message").textContent = "";
      if (res.status == "200") {
        res.json().then((resData) => {
          document.querySelector(".translator_target_textarea").value =
            resData.translations[0].text;
        });
      } else {
        switch (res.status) {
          case 400:
            document.querySelector(".translator_target_textarea").value =
              res.status +
              "\nBad request. Please check error message and your parameters.";
            break;
          case 403:
            document.querySelector(".translator_target_textarea").value =
              res.status +
              "\nAuthorization failed. Please supply a valid auth_key parameter.";
            break;
          case 404:
            document.querySelector(".translator_target_textarea").value =
              "\nThe requested resource could not be found.";
            break;
          case 413:
            document.querySelector(".translator_target_textarea").value =
              res.status + "\nThe request size exceeds the limit.";
            break;
          case 429:
            document.querySelector(".translator_target_textarea").value =
              res.status +
              "\nToo many requests. Please wait and resend your request.";
            break;
          case 456:
            document.querySelector(".translator_target_textarea").value =
              res.status +
              "\nQuota exceeded. The character limit has been reached.";
            break;
          case 503:
            document.querySelector(".translator_target_textarea").value =
              res.status + "\nResource currently unavailable. Try again later.";
            break;
          default:
            document.querySelector(".translator_target_textarea").value =
              res.status + "\nInternal error.";
        }
      }
    });
  }

  document.querySelector("#target_lang").addEventListener("change", (e) => {
    if (document.querySelector(".translator_source_textarea").value != "") {
      target_lang = e.target.value;
      api_translate(
        document.querySelector(".translator_source_textarea").value,
        target_lang,
        api_key
      );
    }
  });

  document
    .querySelector(".translator_source_textarea")
    .addEventListener("keydown", (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        if (document.querySelector(".translator_source_textarea").value != "") {
          target_lang = document.querySelector("#target_lang").value;
          api_translate(
            document.querySelector(".translator_source_textarea").value,
            target_lang,
            api_key
          );
          let save_settings = eel.py_save_settings(
            target_lang,
            command,
            api_key,
            freeFlag
          )();
          save_settings.then((res) => {});
        }
      }
    });

  document.querySelector(".settings_icon").addEventListener("click", (e) => {
    eel.py_open_options()();
    window.open("options.html", "_parent");
  });

  document.querySelector("#ocr_btn").addEventListener("click", (e) => {
    if (ocrFlag == "False") {
      ocrFlag = "True";
    } else {
      ocrFlag = "False";
    }
    eel.py_save_ocr_settings(ocrFlag);
  });
});
