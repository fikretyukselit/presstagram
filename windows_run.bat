@REM Ensure deps Python
for /F %%i in (presstagram_backend\requirements.txt) do python -m pip install %%i

@REM Ensure deps Node
cd presstagram_frontend
npm install

@REM Build and serve frontend
npm run build
start serve -s build -p 80 --cors

@REM Run backend
cd ..
python -m presstagram_backend
