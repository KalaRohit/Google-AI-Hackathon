// Receive message from the popup
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse){
    if(request.message == "turn_blue"){
        document.body.style.backgroundColor = "blue";
    }
})