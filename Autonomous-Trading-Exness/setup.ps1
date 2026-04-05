# Setup Script for "my drive projects"
# IMPORTANT: Before running this script, ensure you have set up your .env file
# with *new*, secure API keys and tokens. The previous ones have been exposed.

$ProjectPath = "C:\my drive projects"

# Create the main directory
If (!(Test-Path $ProjectPath)) {
    New-Item -ItemType Directory -Force -Path $ProjectPath
    Write-Host "Created directory: $ProjectPath" -ForegroundColor Green
} else {
    Write-Host "Directory already exists: $ProjectPath" -ForegroundColor Yellow
}

Set-Location $ProjectPath

# --- Clone Repositories ---
Write-Host "Cloning repositories..." -ForegroundColor Cyan

# 1. Mouyleng172 Repo
$MouylengRepo = "https://github.com/Mouy-leng172.git"
Write-Host "Cloning $MouylengRepo"
git clone $MouylengRepo

# 2. Forgejo Runner
$ForgejoRepo = "https://code.forgejo.org/forgejo/runner.git"
Write-Host "Cloning $ForgejoRepo"
git clone $ForgejoRepo

# 3. MQL5 Forge Repo
$MQL5Repo = "https://forge.mql5.io/LengKundee/A6..9V-GenX_FX.main.git"
Write-Host "Cloning $MQL5Repo"
git clone $MQL5Repo


# --- Download F-Droid APK ---
Write-Host "Downloading F-Droid.apk..." -ForegroundColor Cyan
$FDroidUrl = "https://f-droid.org/F-Droid.apk"
$FDroidDest = Join-Path -Path $ProjectPath -ChildPath "F-Droid.apk"

Try {
    Invoke-WebRequest -Uri $FDroidUrl -OutFile $FDroidDest
    Write-Host "Successfully downloaded F-Droid.apk to $FDroidDest" -ForegroundColor Green
} Catch {
    Write-Host "Error downloading F-Droid.apk: $_" -ForegroundColor Red
}

Write-Host "Setup complete in $ProjectPath!" -ForegroundColor Green
Write-Host "Next steps:"
Write-Host "1. Review the cloned repositories."
Write-Host "2. Copy the .env.template to .env and fill in your NEW secure credentials."
Write-Host "3. Refer to the specific READMEs in each repository for further setup instructions."
