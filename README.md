python -m venv env

cmd: 
    venv\Scripts\activate
PowerShell:
    .\venv\Scripts\Activate.ps1
Git Bash:
    source venv/Scripts/activate

python -m pip install --upgrade pip

python -m pip install django-compressor