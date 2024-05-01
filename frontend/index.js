document.addEventListener("DOMContentLoaded", onDocumentLoad);
function onDocumentLoad() {
  let checkbox = document.getElementById("flexSwitchCheckDefault");
  let select = document.getElementById("ReadingLevel");
  let spinner = document.getElementById("spinner");
  let mainbody = document.getElementById("main-body");
  let chatButton = document.getElementById("start-chat")

  select.addEventListener("change", outputSelection);
  checkbox.addEventListener("click", toggleSimplification);
  chatButton.addEventListener("click", startChatEvent)

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

async function getUserCredentials() {
  const userCredentialFilePath = chrome.runtime.getURL("creds.json");
  let credsFile = await fetch(userCredentialFilePath);
  let credsFileData = await credsFile.json();

  return credsFileData;
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

let userMessageHistory = []
const startChatEvent = (e) => {
  let chatButton = document.getElementById("start-chat");
  let chatWindow = document.getElementById("chat-window");
  let body = document.getElementById("resizable");
  let submitButton = document.getElementById("submit-button");
  submitButton.addEventListener("click", websiteChatCall);
  chatButton.style.display = "none";
  chatWindow.style.display = "flex";
  body.classList.add("increase-animation");

  let userMessage = document.getElementById("chat-input").value;

  console.log(userMessage);
}

const fetchWebsiteData = async () => {
  return new Promise((resolve, reject) => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (chrome.runtime.lastError) {
        reject(new Error(chrome.runtime.lastError.message));
        return;
      }

      chrome.tabs.sendMessage(tabs[0].id, { message: "get_webpage_content" }, (response) => {
        if (chrome.runtime.lastError) {
          reject(new Error(chrome.runtime.lastError.message));
        } else {
          resolve(response);
        }
      });
    });
  });
};

const websiteChatCall = async () => {
  let chatInput = document.getElementById("user-input");
  let userMessage = chatInput.value;

  const userMessageElement = document.createElement('p');
  userMessageElement.textContent = userMessage;
  userMessageElement.classList.add("human-messages");
  document.getElementById('messages').appendChild(userMessageElement);
  chatInput.value = "";

  let webpageScrapeResponse = await fetchWebsiteData();
  let webpageData = webpageScrapeResponse.content;

  const req_object = JSON.stringify({
    request_id: "asfdadsf",
    messages: userMessageHistory,
    newQuestion: userMessage,
    webpageContent: webpageData
  })

  console.log(req_object);

  let userCreds = await getUserCredentials();
  let userCredsData = await userCreds;
  let apiKey = userCredsData.apikey;

  

  const response = await fetch(`https://simple-script-api-bplyx02o.uc.gateway.dev/v1/model/gemini-pro:chat?key=${apiKey}`, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: req_object
  })

  modelOutput = await response.json();
  const modelMessageElement = document.createElement('p');
  modelMessageElement.textContent = modelOutput;
  modelMessageElement.classList.add("model-messages");
  document.getElementById('messages').appendChild(modelMessageElement);

  const userMessageObject = {
    role: "user",
    parts: [userMessage]
  };

  const modelMessageObject = {
    role: "model",
    parts: [modelOutput]
  };

  userMessageHistory.push(userMessageObject);
  userMessageHistory.push(modelMessageObject);

  console.log("history: ",userMessageHistory)


  console.log(modelOutput);
  console.log("usermessage",  userMessage);
}