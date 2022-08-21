param([string]$wd = "")

Write-Output "Sleeping to let things initialize..."
Start-Sleep -Seconds 30.0
Write-Output "Done Sleep"

Set-Location $wd

Write-Output "Init virtual enviroment"
.\.venv\Scripts\Activate.ps1

Write-Output "Installing pip requirements"
pip install -r .\requirements.txt

Write-Output "Starting Script"
py -3.10 .\discord_notif_system_util.py