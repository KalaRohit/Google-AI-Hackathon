document.addEventListener("DOMContentLoaded", onDocumentLoad);
function onDocumentLoad() {
  let checkbox = document.getElementById("flexSwitchCheckDefault");
  let select = document.getElementById("ReadingLevel");
  let spinner = document.getElementById("spinner");
  let mainbody = document.getElementById("main-body");

  select.addEventListener("change", outputSelection);
  checkbox.addEventListener("click", toggleSimplification);

  function toggleSimplification() {
    console.log("toggled!");
    spinner.style.display = "block";
    mainbody.style.display = "none";
    
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

chrome.runtime.onMessage.addListener(
    async function(req, sender, sendResponse) {
      let spinner = document.getElementById("spinner");
      let mainbody = document.getElementById("main-body");
      console.log("received message back!")
      if(req.message === "simplify-complete"){
        spinner.style.display = "none";
        mainbody.style.display = "block"; 
    }
  }
)
