@REM Kill the frontend
taskkill /F /IM "node.exe" /T

@REM Kill the backend
taskkill /F /IM "python.exe" /T

taskkill /F /IM "cmd.exe" /T
