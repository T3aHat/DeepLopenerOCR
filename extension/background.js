chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.message == "translating") {
    chrome.windows.update(
      sender.tab.windowId,
      { focused: true },
      function (tab) {}
    );
  }
  sendResponse();
});
