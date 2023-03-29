# Check if python3.11 or above is present
if (Get-Command python -ErrorAction SilentlyContinue) {
    $python_version = python --version | Select-String -Pattern "\d+\.\d+\.\d+" | Foreach-Object { $_.Matches.Value }
    $major_version = $python_version.Split('.')[0]
    $minor_version = $python_version.Split('.')[1]
    if ($major_version -gt 3 -or ($major_version -eq 3 -and $minor_version -ge 11)) {
        Write-Host "Python version $python_version is installed."
    } else {
        Write-Host "Python version $python_version is not supported!"
        Write-Host "Install Python 3.11 or higher and then restart this setup."
        exit
        # $install_python = Read-Host "Do you want to install the latest version of Python3? (Y/N)"
        # if ($install_python -eq "Y" -or $install_python -eq "y") {
        #     $latest_version = (Invoke-WebRequest "https://www.python.org/downloads/" -UseBasicParsing).Content | Select-String -Pattern "Download Python \d+\.\d+\.\d+"
        #     $latest_version = $latest_version.Matches.Value -replace "Download Python ", ""
        #     Write-Host "Installing Python $latest_version..."
        #     Start-Process "https://www.python.org/ftp/python/$latest_version/python-$latest_version-amd64.exe"
        # }
    }
} else {
    Write-Host "Python is not installed!"
    Write-Host "Install Python 3.11 or higher and then restart this setup."
    exit
    # $install_python = Read-Host "Do you want to install Python 3.11? (Y/N)"
    # if ($install_python -eq "Y" -or $install_python -eq "y") {
    #     $latest_version = (Invoke-WebRequest "https://www.python.org/downloads/" -UseBasicParsing).Content | Select-String -Pattern "Download Python \d+\.\d+\.\d+"
    #     $latest_version = $latest_version.Matches.Value -replace "Download Python ", ""
    #     Write-Host "Installing Python $latest_version..."
    #     Start-Process "https://www.python.org/ftp/python/$latest_version/python-$latest_version-amd64.exe"
    # }
}

Write-Host "Creating dev virtual environment..."
python -m venv venv

Write-Host "Activating virtual environment..."
.\venv\Scripts\Activate.ps1

Write-Host "Installing dependencies in virtual environment..."
pip install -r requirements.txt

Write-Host ""
Write-Host "Lamina dev environment setup SUCCESS"
