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
    $contents | Out-File $pyFile -Encoding ASCII
}

function FixAscii($file) {
    # read contents of $file
    $contents = Get-Content $file -Raw
    #make new file with _new appended to the end
    $newFile = $file -Replace "\.py" , "_new.py"
    Write-Host $newFile
    # write new file
    $contents | Out-File $newFile -Encoding ASCII
    # delete old file
    Remove-Item $file
    # rename new file to old file
    Rename-Item $newFile $file
}

# get full file path of all .js files in the python directory
$pythonDir = 'python'
# $jsFiles = Get-ChildItem -Path $pythonDir -Filter *.js -Recurse -File | Select-Object -ExpandProperty FullName
$pyFiles = Get-ChildItem -Path $pythonDir -Filter *.py -Recurse -File | Select-Object -ExpandProperty FullName
# convert each file to python
foreach ($file in $pyFiles) {
    Write-Host $file 
    FixAscii $file
}
