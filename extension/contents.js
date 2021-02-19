document.querySelector(".hidemessage").textContent = "extension installed!";
chrome.runtime.sendMessage({ message: "get_windowid" }, function (res) {
  if (chrome.runtime.lastError) {
  }
  windowid = res;
  const hidemessageDOM = document.querySelector(".hidemessage");
  const observer = new MutationObserver((records) => {
    if (hidemessageDOM.textContent == "minimize") {
      hidemessageDOM.textContent = "";
      chrome.runtime.sendMessage({ message: "minimize" }, function (res) {
        if (chrome.runtime.lastError) {
        }
      });
    } else if (hidemessageDOM.textContent == "translating...") {
      chrome.runtime.sendMessage(
        { message: "active", windowid: windowid },
        function (res) {
          if (chrome.runtime.lastError) {
          }
        }
      );
    } else if (hidemessageDOM.textContent == "close") {
      hidemessageDOM.textContent = "";
      chrome.runtime.sendMessage(
        { message: "close", winid: windowid },
        function (res) {
          if (chrome.runtime.lastError) {
          }
        }
      );
    }
  });
  observer.observe(hidemessageDOM, {
    characterData: true,
    attributes: true,
    childList: true,
  });

  const messageDOM = document.querySelector(".message");
  const mobserver = new MutationObserver((records) => {
    if (messageDOM.textContent == "translating...") {
      chrome.runtime.sendMessage(
        { message: "active", windowid: windowid },
        function (res) {
          if (chrome.runtime.lastError) {
          }
        }
      );
    }
  });
  mobserver.observe(messageDOM, {
    characterData: true,
    attributes: true,
    childList: true,
  });
});
