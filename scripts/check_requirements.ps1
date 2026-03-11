#!/usr/bin/env pwsh
<#
.SYNOPSIS
    TeacherManager - Check prerequisites for development.
.DESCRIPTION
    Verifies Python 3.12+, Poetry, Docker, and other dependencies.
    Run this locally and paste the output into chat.
.EXAMPLE
    .\scripts\check_requirements.ps1
#>

$ErrorActionPreference = "SilentlyContinue"
$FailureCount = 0
$line = "========================================"

Write-Host $line -ForegroundColor Cyan
Write-Host "TeacherManager - Prerequisites Check" -ForegroundColor Cyan
Write-Host $line -ForegroundColor Cyan
Write-Host ""

# ---------- Python 3.12+ ----------
Write-Host "[1/7] Checking Python 3.12+..." -ForegroundColor Yellow
$pythonVersion = python --version
if ($LASTEXITCODE -eq 0) {
    Write-Host "  OK: $pythonVersion"
    if ($pythonVersion -match "3\.12|3\.13|3\.14") {
        Write-Host "  OK: Python version is 3.12+" -ForegroundColor Green
    }
    else {
        Write-Host "  ERROR: Python version must be 3.12 or higher" -ForegroundColor Red
        $FailureCount++
    }
}
else {
    Write-Host "  ERROR: Python not found or not in PATH" -ForegroundColor Red
    Write-Host "  Install Python 3.12+ from https://www.python.org/downloads/" -ForegroundColor Magenta
    $FailureCount++
}
Write-Host ""

# ---------- Poetry ----------
Write-Host "[2/7] Checking Poetry..." -ForegroundColor Yellow
$poetryVersion = poetry --version
if ($LASTEXITCODE -eq 0) {
    Write-Host "  OK: $poetryVersion" -ForegroundColor Green
}
else {
    Write-Host "  ERROR: Poetry not found" -ForegroundColor Red
    Write-Host "  Install: pip install poetry" -ForegroundColor Magenta
    $FailureCount++
}
Write-Host ""

# ---------- PostgreSQL Client ----------
Write-Host "[3/7] Checking PostgreSQL client..." -ForegroundColor Yellow
$psqlVersion = psql --version
if ($LASTEXITCODE -eq 0) {
    Write-Host "  OK: $psqlVersion" -ForegroundColor Green
}
else {
    Write-Host "  WARNING: PostgreSQL client not found (optional if using Docker)" -ForegroundColor Yellow
    Write-Host "  Install: https://www.postgresql.org/download/windows/" -ForegroundColor Magenta
}
Write-Host ""

# ---------- Docker ----------
Write-Host "[4/7] Checking Docker..." -ForegroundColor Yellow
$dockerVersion = docker --version
if ($LASTEXITCODE -eq 0) {
    Write-Host "  OK: $dockerVersion" -ForegroundColor Green
}
else {
    Write-Host "  ERROR: Docker not found" -ForegroundColor Red
    Write-Host "  Install: https://www.docker.com/products/docker-desktop" -ForegroundColor Magenta
    $FailureCount++
}
Write-Host ""

# ---------- Git ----------
Write-Host "[5/7] Checking Git..." -ForegroundColor Yellow
$gitVersion = git --version
if ($LASTEXITCODE -eq 0) {
    Write-Host "  OK: $gitVersion" -ForegroundColor Green
}
else {
    Write-Host "  ERROR: Git not found" -ForegroundColor Red
    Write-Host "  Install: https://git-scm.com/download/win" -ForegroundColor Magenta
    $FailureCount++
}
Write-Host ""

# ---------- Redis (optional) ----------
Write-Host "[6/7] Checking Redis (optional - Docker fallback OK)..." -ForegroundColor Yellow
$redisVersion = redis-cli --version
if ($LASTEXITCODE -eq 0) {
    Write-Host "  OK: $redisVersion" -ForegroundColor Green
}
else {
    Write-Host "  WARNING: Redis not found (use docker compose instead)" -ForegroundColor Yellow
}
Write-Host ""

# ---------- .env exists ----------
Write-Host "[7/7] Checking .env file..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "  OK: .env file found" -ForegroundColor Green
}
else {
    Write-Host "  WARNING: .env file not found" -ForegroundColor Yellow
    Write-Host "  Run: Copy-Item .env.example .env" -ForegroundColor Magenta
}
Write-Host ""

# ---------- Summary ----------
Write-Host $line -ForegroundColor Cyan
if ($FailureCount -eq 0) {
    Write-Host "OK: All critical checks passed!" -ForegroundColor Green
}
else {
    Write-Host "ERROR: $FailureCount critical check(s) failed" -ForegroundColor Red
    Write-Host "Please install missing dependencies and re-run this script." -ForegroundColor Red
}
Write-Host $line -ForegroundColor Cyan
Write-Host ""

exit $FailureCount
