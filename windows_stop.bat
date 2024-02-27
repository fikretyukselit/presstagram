@REM Kill the frontend
taskkill /F /IM "serve.exe" /T

@REM Kill the backend
taskkill /F /IM "python.exe" /T
