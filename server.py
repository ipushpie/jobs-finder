from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os
import uvicorn

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables to track process status
process_status = {
    'status': 'idle',  # idle, processing, completed, error
    'message': '',
}

def run_script():
    """Run the main.py script"""
    try:
        process_status['status'] = 'processing'
        process_status['message'] = 'Running job scraper...'

        # Run the main.py script
        result = subprocess.run(['python', 'main.py'],
                               capture_output=True,
                               text=True)

        if result.returncode == 0:
            process_status['status'] = 'completed'
            process_status['message'] = 'CSV file generated successfully'
        else:
            process_status['status'] = 'error'
            process_status['message'] = f'Error running script: {result.stderr}'
            print(f"Error: {result.stderr}")
    except Exception as e:
        process_status['status'] = 'error'
        process_status['message'] = f'Exception: {str(e)}'
        print(f"Exception: {str(e)}")

@app.post("/start")
async def start_process(background_tasks: BackgroundTasks):
    """Start the job scraping process"""
    # Only start if not already processing
    if process_status['status'] == 'processing':
        return JSONResponse(
            content={
                'status': 'error',
                'message': 'Process already running'
            },
            status_code=400
        )

    # Reset status
    process_status['status'] = 'processing'
    process_status['message'] = 'Starting process...'

    # Start the process in the background
    background_tasks.add_task(run_script)

    return {
        'status': 'started',
        'message': 'Process started'
    }

@app.get("/status")
async def get_status():
    """Get the current status of the process"""
    return {
        'status': process_status['status'],
        'message': process_status['message']
    }

@app.get("/download")
async def download_file():
    """Download the generated CSV file"""
    if process_status['status'] != 'completed':
        raise HTTPException(
            status_code=400,
            detail="CSV file not ready yet"
        )

    # Check if file exists
    if not os.path.exists('jobs.csv'):
        raise HTTPException(
            status_code=404,
            detail="CSV file not found"
        )

    return FileResponse(
        path='jobs.csv',
        filename='linkedin_jobs.csv',
        media_type='text/csv'
    )

if __name__ == '__main__':
    print("Starting server on http://localhost:5000")
    uvicorn.run(app, host="0.0.0.0", port=5000)
