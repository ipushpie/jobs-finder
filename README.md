# LinkedIn Job CSV Downloader Extension

A Chrome extension that downloads LinkedIn job data as a CSV file with one click.

## Prerequisites

Before using this extension, you need to install the required Python packages:

```bash
pip install fastapi uvicorn
```

## How to Install the Extension

1. Open Chrome browser
2. Type `chrome://extensions/` in the address bar and press Enter
3. Enable "Developer mode" by toggling the switch in the top-right corner
4. Click on "Load unpacked" button
5. Navigate to the `extension` folder in this project and select it
6. The extension should now appear in your extensions list

## How to Use

### Step 1: Start the Server
Before using the extension, you need to start the server:

1. Open a terminal/command prompt
2. Navigate to your project directory
3. Run the server with:
   ```
   python server.py
   ```
4. You should see a message: "Starting server on http://localhost:5000"
5. Keep this terminal window open while using the extension

### Step 2: Use the Extension
1. Click on the extension icon in your Chrome toolbar
2. A popup will appear with a "Download Jobs CSV" button
3. Click the button to start the process
4. You'll see a loading spinner while the script runs (this may take a few minutes)
5. Once complete, the CSV file will be downloaded automatically
6. If there's an error, you'll see an error message in the popup

## Important Notes
- The server must be running for the extension to work
- The extension communicates with the server on localhost:5000
- The script may take several minutes to run as it scrapes job data
- The CSV file will be saved to your default downloads folder unless you choose a different location
