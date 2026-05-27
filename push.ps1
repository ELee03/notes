param([string]$msg = "Update notes")
git add index.html style.css control/ -v
git commit -m $msg
git push
