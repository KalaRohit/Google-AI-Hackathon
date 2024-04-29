let simplify = false;
let simplifyGrade = 7;
let memoized = {};

chrome.runtime.onMessage.addListener(
    async function(req, sender, sendResponse){ 
        if(req.message === "switch_text"){ 
            document.querySelectorAll('p')
                .forEach(async (p) => {
                    simplifyDocument(p);
                }); 
        }

        if (req.message === "change_grade"){ 
            simplifyGrade = req.grade;
        } 
    }
)

async function getUserCredentials() {
    const userCredentialFilePath = chrome.runtime.getURL("creds.json");
    let credsFile = await fetch(userCredentialFilePath);
    let credsFileData = await credsFile.json();

    return credsFileData;
}

async function simplifyDocument(p) {
    const model_output = await simplifyText(p.textContent);
    p.textContent =  model_output;
}

async function simplifyText(textContent) {
    var request_obj = {
        "request_id": "1",
        "text": textContent,
        "target_reading_level": simplifyGrade
    };

    console.log(request_obj);
    
    let userCreds = await getUserCredentials();
    let userCredsData = await userCreds;
    let apiKey = userCredsData.apikey;

    const repsonse = await fetch(`https://simple-script-api-bplyx02o.uc.gateway.dev/v1/model/gemini-pro:simplify?key=${apiKey}`, {
        method: "POST",
        body: JSON.stringify(request_obj),
        headers: {
            'Content-Type': 'application/json'
        }
    });

    const model_output = await repsonse.json();

    return model_output;
}


