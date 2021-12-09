const target = document.querySelector(".message");
const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    if (document.querySelector(".message").textContent != "") {
      chrome.runtime.sendMessage({ message: "translating" }, function (res) {
        if (chrome.runtime.lastError) {
        }
      });
    }
  });
});
const config = {
  childList: true,
};
observer.observe(target, config);
