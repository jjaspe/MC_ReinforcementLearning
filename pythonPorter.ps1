# this PowerShell function takes a file, changes the extension to .py and appends a string to the end of it

function ConvertToPython($file) {
    # read contents of $file
    $contents = Get-Content $file 
    # put # at the start of every line
    $contents = $contents | ForEach-Object { "# $_" }    
    # append the string to the end of the file
    $prompt = '# the following is the above commented javascript code converted to python'
    $contents += "`n`n$prompt`n`n"
    $pyFile = $file -Replace ".js" , ".py"
    # write python file
    $contents | Out-File $pyFile
}

# get full file path of all .js files in the python directory
$pythonDir = 'python'
$jsFiles = Get-ChildItem -Path $pythonDir -Filter *.js -Recurse -File | Select-Object -ExpandProperty FullName

# convert each file to python
foreach ($file in $jsFiles) {
    Write-Host $file
    ConvertToPython $file
}
