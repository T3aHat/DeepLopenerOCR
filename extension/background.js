chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.message == "minimize") {
    chrome.windows.getCurrent((window) => {
      chrome.windows.update(window.id, { state: "minimized" });
    });
  } else if (request.message == "get_windowid") {
    chrome.windows.getCurrent((window) => {
      sendResponse(window.id);
    });
  } else if (request.message == "active") {
    chrome.windows.update(request.windowid, {
      focused: true,
    });
  } else if (request.message == "close") {
    chrome.windows.remove(request.winid);
  }
  return true;
});

var isOptions = false;
chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
  if (tab.url == "http://localhost:8000/options.html") {
    isOptions = true;
  } else {
    isOptions = false;
  }
});
