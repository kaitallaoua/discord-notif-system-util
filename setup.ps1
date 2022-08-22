Write-Host "Init python 3.10 virtual enviroment"
py -3.10 -m venv .venv

Write-Host "Activate virtual env"
.\.venv\Scripts\Activate.ps1

Write-Host "Install requirements"
pip install -r .\requirements.txt

Write-Output "Done"