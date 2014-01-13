// This is the background extension script. It does the following:
// - Sniff headers and send to the native python code.
// - Receive messages from content scripts (containing page source) and pass on to the native python code.
// - Receive messages from native python code and change badge accordingly.

// Used to connect to the native application
var port = null;

// Verbosity level of messages can be set via the extensions's options page
var verbose = (localStorage["verbosity"] === 'verbose');

// Init a connection to the native application
connect();

// Wait for a message from the content script. The message contains the full page source
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    // If this is a message from a content script, pass it along to the native application
    if (sender.tab) {
      contents = {'url': sender.tab.url, 'pagecontent': request.pagecontent};
      message = {'msgtype': 'content',
                 'content': contents};
      sendNativeMessage(message);
    }
  });

// Whenever we send a request, pipe it to the application
chrome.webRequest.onSendHeaders.addListener(
  function(details) {    
    if (verbose) {
      // Send all request parameters and headers to the native application
      sendNativeMessage(details);
    } else {
      // Only process GET requests for main_frames
      if ((details.method === 'GET') && (details.type === 'main_frame')) {
        var short_details = {
          //'requestId': details.requestId, 
          'url': details.url,
          //'method': details.method,
          //'type': details.type,
          'requestHeaders': details.requestHeaders
        };
        message = {'msgtype': 'request',
                    'content': short_details};
        sendNativeMessage(message);
      }
    }
  },
  {urls: ["<all_urls>"]},
  ["requestHeaders"]);
 
// Whenever we complete a request, pipe it to the application
/*
chrome.webRequest.onCompleted.addListener(
  function(details) {    
    if (verbose) {
      // Send all request parameters and headers to the native application
      sendNativeMessage(details);
    } else {
      // Only process GET requests for main_frames
      if ((details.method === 'GET') && (details.type === 'main_frame')) {
        var short_details = {
          'requestId': details.requestId, 
          'url': details.url,
          'method': details.method,
          'type': details.type,
          'responseHeaders': details.responseHeaders
        };
        sendNativeMessage(short_details);
      }
    }
  },
  {urls: ["<all_urls>"]},
  ["responseHeaders"]);
  */

// Connect to the native application
function connect() {
  var hostName = "com.multisurf";
  console.log('Connecting to native messaging host ' + hostName);
  port = chrome.runtime.connectNative(hostName);
  port.onMessage.addListener(onNativeMessage);
  port.onDisconnect.addListener(onDisconnected);
}

// Send message to native application
function sendNativeMessage(message) {
  if (null == port) {
    connect();
  }
    
  port.postMessage(message);
  console.log('Sent message: ' + JSON.stringify(message));
}

// Receive message from native application
function onNativeMessage(message) {
  console.log('Received message: ' + JSON.stringify(message));
  
  // If this is a badge message, change badge state
  if (message.hasOwnProperty('badge')) {
    setBadge(message.badge === 'safe')
  }
}

function onDisconnected() {
  console.log('Disconnected from native app. LastError: ' + chrome.runtime.lastError.message);
  port = null;
}

// Change badge text and color
function setBadge(safeState) {
  if (safeState) {
    chrome.browserAction.setBadgeText({"text": localStorage["safe_string"]});
    chrome.browserAction.setBadgeBackgroundColor({color: [0, 255, 0, 255]});
  } else {
    chrome.browserAction.setBadgeText({"text": localStorage["warning_string"]});
    chrome.browserAction.setBadgeBackgroundColor({color: [255, 0, 0, 255]});  
  }
}
