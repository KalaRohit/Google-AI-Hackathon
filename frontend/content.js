// Receive message from the popup
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse){
    if(request.message == "switch_text"){
        document.querySelectorAll('p').forEach(switchText);
    }
})

function switchText(p) {
    // pass p to backend, and get the response here
    p.textContent = "Gemini Response";
}

