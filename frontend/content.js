// Receive message from the popup
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse){
    if(request.message == "switch_text"){
        // Only <p> elements will be simplified
        document.querySelectorAll('p').forEach(switchText);
    }
})

async function switchText(p) {
    // pass p to backend, and get the model output
    const model_output = await simplifyText(p);
    p.textContent =  model_output.fact;
}

async function simplifyText(p) {
    // This is the object being sent to the server
    var request_obj = {
        "request_id": "1",
        "text": p,
        "target_reading_level": 3
    }

    // const repsonse = await fetch("http://gai.hackathon.rohitkala.com/backend/v1/model/gemini-pro:summarize", {
    //     method: "POST",
    //     body: JSON.stringify(request_obj)
    // });

    const repsonse = await fetch("https://catfact.ninja/fact", {
        method: "GET"
    });

    const model_output = await repsonse.json();

    return model_output;
}


