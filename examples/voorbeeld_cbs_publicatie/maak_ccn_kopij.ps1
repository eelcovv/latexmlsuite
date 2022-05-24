<#
.SYNOPSIS
  Maak alle files mbv latex2ccn om je kopij aan te leveren
.DESCRIPTION
  Zorg dat latex2cnn in je pad staat en je miktex geinstalleerd hebt
.PARAMETER script_name
    Naam van het lanceerscript.
.PARAMETER gmake
    Gebruik gmake ipv make als make exe
.PARAMETER settings_file
    Naam van de settings file. Default is 'rapport_settings.yml', dus je mag het ook weglaten
.PARAMETER help
    Laat de help van deze script zien
.PARAMETER test
    Laat zien welke commando dit script aan gaat roepen
.PARAMETER dryrun
    Laat alleen de commandos zien die aangeroepen worden zonder ze uit te voeren
.PARAMETER mode
    Geef de modus van het script. Geldig zijn 'all', 'latex', 'xml', 'html' of 'none'. Default = 'all'
    all:   doorloop alle stappen.
    latex: maak alleen de latex pdf
    xml: maak alleen de xml vanuit de tex files. Langzame stap
    html: converteer de xml naar html
    none: doe niks, maar run alleen de makefiles
.EXAMPLE
    maak_ccn_kopij.ps1
    Doorloop alle stappen om de kopij te maken
.EXAMPLE
    maak_ccn_kopij.ps1 -mode latex
    Maak alleen de pdf vanuit de latex code
.EXAMPLE
    maak_ccn_kopij.ps1 -dryrun
    Laat alleen de commandos zien die latex2cnn genereert om de kopij te make
#>
[CmdletBinding()]
param (
    [string]$script_name = "latex2ccn",
    [string]$settings_file = "rapport_settings.yml",
    [switch]$test = $false,
    [switch]$dryrun = $false,
    [switch]$gmake = $false,
    [switch]$vv = $false,
    [switch]$help = $false,
    [ValidateSet('all', 'latex', 'xml', 'html', 'none')]
    [string]$mode="all"
)

if($help){
    Get-Help $MyInvocation.InvocationName -detailed
    exit
}
if ($dryrun){
    $dryrun_optie = "--test"
}
else{
    $dryrun_optie = ""
}
if ($vv){
    $debug_optie = "--debug"
}
else{
    $debug_optie = ""
}
if ($gmake){
    $make_optie = "--make_exe gmake"
}
else{
    $make_optie = ""
}


$cmd="$script_name
      --settings_filename $settings_file
      $dryrun_optie
      $make_optie
      $debug_optie
      --mode $mode
"
$cmd = $cmd -replace '\s+', ' '
Write-Output "Start script..."
Write-Output $cmd
Write-Output "============= begin output script ========= "
if  (-Not $test) {
    Invoke-Expression $cmd
}
Write-Output "============= eind output script ========= "
Write-Output "Done!"
