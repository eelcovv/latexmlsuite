$TOOLS_DIR = "\\\\cbsp.nl\\Productie\\secundair\\DecentraleTools\\Output\\CBS_Python\Python3.9"
$cmd="pip install . --no-build-isolation --prefix $TOOLS_DIR -U"
$cmd = $cmd -replace '\s+', ' '
Write-Output $cmd
Invoke-Expression $cmd


