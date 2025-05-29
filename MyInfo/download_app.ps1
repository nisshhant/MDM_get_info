# Check for Administrator rights
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)) {
    Write-Output "Restarting with elevated privileges..."
    Start-Process powershell "-ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

# Brave browser stable offline installer URL (official)
$braveUrl = "https://github.com/brave/brave-browser/releases/latest/download/BraveBrowserSetup.exe"

# Temporary path to save the installer
$tempPath = "$env:TEMP\BraveBrowserSetup.exe"

try {
    Write-Output "Downloading Brave Browser installer..."
    Invoke-WebRequest -Uri $braveUrl -OutFile $tempPath

    Write-Output "Download complete. Starting silent install..."

    # Run installer silently (Brave supports /silent flag)
    $process = Start-Process -FilePath $tempPath -ArgumentList "/silent" -Wait -PassThru

    if ($process.ExitCode -eq 0) {
        Write-Output "Brave Browser installed successfully."
    } else {
        Write-Output "Installer exited with code $($process.ExitCode)."
    }

    # Clean up installer
    Remove-Item $tempPath -Force
    Write-Output "Installer file removed."

} catch {
    Write-Error "Failed to download or install Brave Browser: $_"
}
