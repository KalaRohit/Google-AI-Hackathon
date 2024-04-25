document.addEventListener("DOMContentLoaded", runFunction);
function runFunction() {
  let checkbox = document.getElementById("flexSwitchCheckDefault");
  let select = document.getElementById("ReadingLevel");
  select.addEventListener("change", outputSelection);
  checkbox.addEventListener("click", changeBgColor);
  function changeBgColor() {
    chrome.tabs.query(
      { active: true, currentWindow: true },

      function (tabs) {
        chrome.tabs.sendMessage(tabs[0].id, { message: "switch_text" });
      }
    );
  }
  function outputSelection() {
    var selectedOption = document.getElementById("ReadingLevel").value;
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      chrome.tabs.sendMessage(tabs[0].id, {
        message: "change_grade",
        grade: selectedOption,
      });
    });
  }
}
