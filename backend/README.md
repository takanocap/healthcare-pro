# Create virtual environment

```
python -m venv venv
```

# Activate virtual environment

```
venv\Scripts\activate
```

# Download dependencies

```
<Python executable path> -m pip install --upgrade pip
"c:\google hackathon\healthcare-pro\backend\venv\scripts\python.exe" -m pip install --upgrade pip
pip install -r requirements.txt
```

# Start backend server

```
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```