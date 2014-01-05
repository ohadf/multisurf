// This content script is injected to every web page and sends the page source back to background.js

var html = document.documentElement.outerHTML;
chrome.runtime.sendMessage({pagecontent: html}, function(response) {
  // We don't care about the response.
  // console.log(response);
});
