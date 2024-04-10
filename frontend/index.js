document.addEventListener("DOMContentLoaded", runFunction);

function runFunction() {
    let button = document.getElementById("primary-button");
    button.addEventListener("click", changeBgColor);
    function changeBgColor(){
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs){
            // Send a message to the current tab
            chrome.tabs.sendMessage(tabs[0].id, {message: "switch_text"});
        })
    }
}