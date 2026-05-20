# Aksesa CLI Installer (PowerShell)
# Usage: powershell -c "irm ai.codecircle.space/install.ps1 | iex"

$ErrorActionPreference = "Stop"

$Repo = "oharatech/aksesa-cli"
$BinaryName = "aksesa.exe"
$InstallDir = if ($env:INSTALL_DIR) { $env:INSTALL_DIR } else { "$env:LOCALAPPDATA\AksesaCLI\bin" }

function Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Green
}

function Warn {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor Yellow
}

function Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
    exit 1
}

function Detect-Platform {
    $arch = if ($env:PROCESSOR_ARCHITECTURE -eq "AMD64") { "x86_64" }
            elseif ($env:PROCESSOR_ARCHITECTURE -eq "ARM64") { "aarch64" }
            else { "x86_64" }  # fallback
    return "$arch-pc-windows-msvc"
}

function Get-LatestTag {
    $url = "https://api.github.com/repos/$Repo/releases/latest"
    try {
        $response = Invoke-RestMethod -Uri $url -UseBasicParsing
        return $response.tag_name
    } catch {
        Error "Failed to get latest release tag"
    }
}

function Main {
    Info "Installing Aksesa CLI..."

    $platform = Detect-Platform
    Info "Detected platform: $platform"

    $tag = Get-LatestTag
    Info "Latest version: $tag"

    $archiveName = "aksesa-$tag-$platform.zip"
    $downloadUrl = "https://github.com/$Repo/releases/download/$tag/$archiveName"
    $tmpDir = [System.IO.Path]::GetTempPath() + [System.Guid]::NewGuid().ToString()
    New-Item -ItemType Directory -Path $tmpDir | Out-Null
    $archivePath = Join-Path $tmpDir $archiveName

    Info "Downloading $archiveName..."
    try {
        Invoke-WebRequest -Uri $downloadUrl -OutFile $archivePath -UseBasicParsing
    } catch {
        Error "Failed to download $downloadUrl"
    }

    Info "Extracting..."
    Expand-Archive -Path $archivePath -DestinationPath $tmpDir -Force

    $binaryPath = Join-Path $tmpDir $BinaryName
    if (-not (Test-Path $binaryPath)) {
        # Try finding in subdirectories (onedir fallback, though onefile should be flat)
        $binaryPath = Get-ChildItem -Path $tmpDir -Recurse -Filter $BinaryName | Select-Object -First 1
        if (-not $binaryPath) {
            Error "Expected binary not found after extraction: $BinaryName"
        }
        $binaryPath = $binaryPath.FullName
    }

    if (-not (Test-Path $InstallDir)) {
        Info "Creating install directory: $InstallDir"
        New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
    }

    $destPath = Join-Path $InstallDir $BinaryName
    Info "Installing to $destPath..."
    Copy-Item -Path $binaryPath -Destination $destPath -Force

    # Cleanup
    Remove-Item -Recurse -Force $tmpDir

    # Add to PATH if needed
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($currentPath -notlike "*$InstallDir*") {
        Warn "Adding $InstallDir to your user PATH..."
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$InstallDir", "User")
        $env:Path = "$env:Path;$InstallDir"
    }

    # Verify
    try {
        $version = & $destPath --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Info "Aksesa CLI installed successfully!"
            Info "Version: $version"
        } else {
            Info "Aksesa CLI installed to $destPath"
        }
    } catch {
        Info "Aksesa CLI installed to $destPath"
    }
}

Main
