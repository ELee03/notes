param([string]$msg = "Update notes")

# Build books.json from data/books.yaml
python build.py
if ($LASTEXITCODE -ne 0) {
    Write-Error "build.py failed - aborting deploy"
    exit 1
}

git add -A -v
git commit -m $msg
git push
