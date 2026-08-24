const sessionId="patient-"+Date.now();

const chatBox=document.getElementById("chatBox");
const input=document.getElementById("messageInput");
const sendButton=document.getElementById("sendButton");

function addMessage(text,type){

const div=document.createElement("div");

div.className=`message ${type}`;

div.innerText=text;

chatBox.appendChild(div);

chatBox.scrollTop=chatBox.scrollHeight;

}

sendButton.addEventListener("click",sendMessage);

input.addEventListener("keydown",e=>{

if(e.key==="Enter"&&!e.shiftKey){

e.preventDefault();

sendMessage();

}

});

async function sendMessage(){

const message=input.value.trim();

if(!message)return;

addMessage(message,"user");

input.value="";

try{

const res=await fetch("/chat",{

method:"POST",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify({

session_id:sessionId,

message:message

})

});

const data=await res.json();

addMessage(data.message,"bot");

const emergency=document.getElementById("emergencyCard");

if(data.next_action==="EMERGENCY"){

emergency.classList.remove("hidden");

document.getElementById("emergencyText").innerText=data.message;

}else{

emergency.classList.add("hidden");

}

}catch(err){

addMessage("Unable to connect to the assistant.","bot");

}

}
let mediaRecorder;
let audioChunks = [];

async function startRecording() {

    const stream =
        await navigator.mediaDevices.getUserMedia({
            audio: true
        });

    mediaRecorder =
        new MediaRecorder(stream);

    audioChunks = [];

    mediaRecorder.ondataavailable =
        event => {

            audioChunks.push(
                event.data
            );
        };

    mediaRecorder.onstop =
        async () => {

            const blob =
                new Blob(
                    audioChunks,
                    {
                        type: "audio/webm"
                    }
                );

            const form =
                new FormData();

            form.append(
                "audio",
                blob,
                "voice.webm"
            );

            const response =
                await fetch(
                    "/voice",
                    {
                        method: "POST",
                        body: form
                    }
                );

            const data =
                await response.json();

            document.getElementById(
                "messageInput"
            ).value = data.text;
        };

    mediaRecorder.start();

    setTimeout(
        () => mediaRecorder.stop(),
        5000
    );
}