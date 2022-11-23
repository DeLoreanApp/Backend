# DeLorian Backend
This is a backend repository for DeLorian app

## How to run
1. If you are using a virtual environment activate it

**Windows**
```bash
<name of venv>\Scripts\activate
```
**Linux**
```bash
./<name of venv>/bin/activate
```

2. Make sure all requirements are installed. If not, run:
```bash
pip install -r requirements.txt
```

3. Finally, run the application
```bash
uvicorn app.main:app
```
