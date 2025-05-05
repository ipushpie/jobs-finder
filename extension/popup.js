document.addEventListener('DOMContentLoaded', function() {
  const downloadBtn = document.getElementById('downloadBtn');
  const statusDiv = document.getElementById('status');
  const loadingDiv = document.getElementById('loading');
  
  downloadBtn.addEventListener('click', function() {
    // Show loading spinner
    downloadBtn.disabled = true;
    loadingDiv.style.display = 'block';
    statusDiv.style.display = 'none';
    
    // Send message to background script to start the process
    chrome.runtime.sendMessage({action: "startProcess"}, function(response) {
      if (response && response.status === 'started') {
        // Background script has started the process
        checkStatus();
      } else {
        showError("Failed to start the process. Please try again.");
      }
    });
  });
  
  function checkStatus() {
    // Poll the server to check if the CSV is ready
    fetch('http://localhost:5000/status')
      .then(response => response.json())
      .then(data => {
        if (data.status === 'completed') {
          // CSV is ready, download it
          chrome.downloads.download({
            url: 'http://localhost:5000/download',
            filename: 'linkedin_jobs.csv',
            saveAs: true
          });
          
          // Show success message
          showSuccess("CSV file has been downloaded successfully!");
        } else if (data.status === 'processing') {
          // Still processing, check again after a delay
          setTimeout(checkStatus, 5000);
        } else if (data.status === 'error') {
          // Error occurred
          showError("An error occurred: " + data.message);
        }
      })
      .catch(error => {
        showError("Failed to connect to the server. Make sure the server is running.");
        console.error('Error:', error);
      });
  }
  
  function showSuccess(message) {
    statusDiv.textContent = message;
    statusDiv.style.backgroundColor = '#d4edda';
    statusDiv.style.color = '#155724';
    statusDiv.style.display = 'block';
    loadingDiv.style.display = 'none';
    downloadBtn.disabled = false;
  }
  
  function showError(message) {
    statusDiv.textContent = message;
    statusDiv.style.backgroundColor = '#f8d7da';
    statusDiv.style.color = '#721c24';
    statusDiv.style.display = 'block';
    loadingDiv.style.display = 'none';
    downloadBtn.disabled = false;
  }
});
