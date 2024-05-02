let simplify = false;
let simplifyGrade = 7;
let memoized = {};
let isLoading = false;
let history = [];

chrome.runtime.onMessage.addListener(
    async function(req, sender, sendResponse){ 
        if(req.message === "switch_text"){
            try {
                await swapParagraphElementText();
            } finally {
                //message to show main body again
                (async () => {
                    const response = await chrome.runtime.sendMessage(
                        {message: "simplify-complete"}
                    );
                    
                })();
            }
        }

        if (req.message === "change_grade"){ 
            simplifyGrade = req.grade;
        } 

        if (req.message === "get_webpage_content") {
            const content = await gatherPElementText();
            sendResponse({content: content})
        }
    }
)

function sleep(milliseconds) {
    return new Promise(resolve => setTimeout(resolve, milliseconds));
}

async function swapParagraphElementText() {
    const promises = Array.from(document.querySelectorAll('p')).map(p => 
        sleep(1500).then(() => simplifyDocument(p))
    );
    await Promise.allSettled(promises);
}


async function getUserCredentials() {
    const userCredentialFilePath = chrome.runtime.getURL("creds.json");
    let credsFile = await fetch(userCredentialFilePath);
    let credsFileData = await credsFile.json();

    return credsFileData;
}

async function simplifyDocument(p) {
    const model_output = await simplifyText(p.textContent);
    memoized.model_output = p.textContent;
    p.textContent =  model_output;
}

async function simplifyText(textContent) {
    var requestObj = {
        "request_id": "1",
        "text": textContent,
        "target_reading_level": simplifyGrade
    };

    let userCreds = await getUserCredentials();
    let userCredsData = await userCreds;
    let apiKey = userCredsData.apikey;

    const repsonse = await fetch(`https://simple-script-api-bplyx02o.uc.gateway.dev/v1/model/gemini-pro:simplify?key=${apiKey}`, {
        method: "POST",
        body: JSON.stringify(requestObj),
        headers: {
            'Content-Type': 'application/json'
        }
    });

    // const repsonse = await fetch(`http://127.0.0.1:8000/v1/model/gemini-pro:simplify`, {
    //     method: "POST",
    //     body: JSON.stringify(requestObj),
    //     headers: {
    //         'Content-Type': 'application/json'
    //     }
    // }); //for dev stuff

    const model_output = await repsonse.json();

    return model_output;
}

async function gatherPElementText() {
    let paragraphs = document.querySelectorAll('p');
    let allText = Array.from(paragraphs).map(p => p.textContent).join('\n');
    
    return allText;
}

function revertSimplification() {
    document.querySelectorAll('p')
        .forEach(async (p) => {
            originalContent = [p.textContent];
            p.textContent = originalContent;
        }); 
}
