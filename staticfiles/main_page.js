console.log("Sanity check from room.js.");

// function loadData() {
//     // Get the data from Django context and parse it safely
//    const dataElement = document.getElementById('data-json');
//    if (!dataElement) {
//        console.error('Data element not found');
//        return;
//    }

//    let data;
//    try {
//        data = JSON.parse(dataElement.textContent);
//    } catch (e) {
//        console.error('Failed to parse data JSON', e);
//        return;
//    }
//    // Create HTML content with the data
//    const content = `
//        <p><strong>Chat ID:</strong> ${data.chat_id}</p>
//        <p><strong>Chat Name:</strong> ${data.chat_name}</p>
//        <p><strong>Chat Type:</strong> ${data.chat_type}</p>
//    `;
//    console.log('Data', data);
//    console.log('Content', content);
//    // Insert the content into the placeholder div
//    document.getElementById('telegramInfo').innerHTML = content;
// }
// Automatically trigger loadData when the page loads
// document.addEventListener('DOMContentLoaded', loadData);
// document.getElementById('deleteWebhook').addEventListener('click', function() { /*to trigger deleteWebook view*/
// var endpoint = '/close/';
// fetch(endpoint)
//    .catch(error => console.error('Error:', error));
// });
function copyToClipboard() { /* to copy to clipboard */
    document.getElementById('copy-button').addEventListener('click', async () => {
    const textToCopy = document.getElementById('text-to-copy').innerText;

    try {
        await navigator.clipboard.writeText(textToCopy);
        alert('Text copied to clipboard!');
    } catch (err) {
        console.error('Failed to copy text: ', err);
        alert('Failed to copy text');
    }
    });
}
function getCSRFToken() { /* csrf token */
   return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}
// function executeScriptAndRedirect(url) {
//     const csrftoken = getCSRFToken();

//     $.ajax({
//         url: '/add_chat/', // URL to your Django view
//         method: 'GET',
//         headers: {
//             'X-CSRFToken': csrftoken
//         },
//         success: function(response) {
//             // Optionally handle the response here
//             console.log(response.output);
//             // Redirect to the external page
//             window.location.href = url;
//         },
//         error: function(error) {
//             console.error('Error:', error);
//         }
//     });
// }

let infoSocket = null

function connect() {
    // Connect to the first WebSocket endpoint for BackgroundTaskConsumer
    // messageSocket = new WebSocket('ws://' + window.location.host + '/ws/message/');

    // messageSocket.onopen = function(event) {
    //     console.log('Message WebSocket is connected.');
    // };

    // messageSocket.onmessage = function(event) {
    //     console.log('Message from server (message channel):', event.data);
    // };

    // messageSocket.onclose = function(event) {
    //     console.log('Message WebSocket is closed.');
    // };

    // messageSocket.onerror = function(error) {
    //     console.log("WebSocket encountered an error: " + error.message);
    //     console.log("Closing the socket.");
    //     messageSocket.close();
    // };

    infoSocket = new WebSocket("ws://" + window.location.host + "/ws/info/");

    // on socket open
    infoSocket.onopen = function (e) {
        console.log("Successfully connected to the WebSocket.");
    }

    // on socket close 
    infoSocket.onclose = function (e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function() {
            console.log("Reconnecting...");
            connect();
        }, 2000);
    }

    // on recieving message on group
    infoSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        const receivedUserID = data.data.django_user_id;

        
        var csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        fetch('/user_info/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({receivedUserID: receivedUserID})
        })
            .then(response => {
                if (response.ok) {
                    showInfo(data.data.message);
                }
                else {
                    receivedData = response.json()
                    alert("User "+ receivedData.username + " is linked to this telegram user: " + receivedData.telegram_user + ". You can not link any other user's channel or group!!!");
                }
            })
            .then(userData => {
                console.log(userData);
                
            })

            .catch(error => console.error('Error:', error));  
    }

    // on error
    infoSocket.onerror = function(err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        infoSocket.close();
    }
}

connect();

function showInfo(data) {
    const telegramInfo = document.getElementById('telegramInfo');
    const channel_name = document.getElementById('channel-name');
    const channel_type = document.getElementById('channel-type');
    const channel_photo = document.getElementById('channel-photo');

    console.log(data.chat_title);
    channel_name.innerText = data.chat_title;
    channel_type.textContent = data.chat_type;
    
    const channel_photo_name = data.chat_title;
    var notificationMessage = document.getElementById('notification-message');

    let channel_photo_url;
    
    channel_photo_url = `/media/channel_photos/` + channel_photo_name + `.jpg`;
    channel_photo.innerHTML = `<img src="${channel_photo_url}" alt="Channel photo" style="width:70px;height:70px;border-radius:50%;">`;

    telegramInfo.classList.add('notification-show');
    
    if (notificationMessage) {
        notificationMessage.remove();
    }  
}