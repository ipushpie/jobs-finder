// Listen for messages from the popup
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.action === "startProcess") {
    // Send request to the server to start the process
    fetch("http://localhost:5000/start", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "started") {
          sendResponse({ status: "started" });
        } else {
          sendResponse({ status: "error", message: data.message });
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        sendResponse({
          status: "error",
          message: "Failed to connect to the server",
        });
      });

    // Return true to indicate that we will send a response asynchronously
    return true;
  }
});
