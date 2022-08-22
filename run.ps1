param([string]$wd = "")

Write-Output "Sleeping to let things initialize..."
Start-Sleep -Seconds 30.0
Write-Output "Done Sleep"

Set-Location $wd

Write-Output "Init virtual enviroment"
.\.venv\Scripts\Activate.ps1

Write-Output "Starting Script"
python .\discord_notif_system_util.py

Write-Output "Done"