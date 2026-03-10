
# ./export-code.ps1
param(
  [string]$BaseDir = (Split-Path -Parent $MyInvocation.MyCommand.Path),
  [string]$OutDir  = (Join-Path $BaseDir 'ExportTxt'),
  [string[]]$IgnoreDirs = @('venv', '.vscode', 'chroma')  # diretórios a ignorar
)

# Cria pasta de saída se não existir
if (-not (Test-Path -LiteralPath $OutDir)) {
  New-Item -ItemType Directory -Path $OutDir | Out-Null
}

Write-Host "[INFO] Exportando para: $OutDir"

# Monta regex para ignorar diretórios (match por segmento de caminho)
# Ex.: \\(venv|\.vscode|chroma)(\\|$)
$escaped = $IgnoreDirs | ForEach-Object {
  # Escapa caracteres especiais para regex
  [Regex]::Escape($_)
}
$ignoreRegex = '\\(' + ($escaped -join '|') + ')(\\|$)'

Get-ChildItem -Path $BaseDir -Recurse -File -Include *.py -Force |
  Where-Object {
    # Ignora arquivos dentro dos diretórios da lista
    $_.FullName -notmatch $ignoreRegex -and
    # Evita reprocessar coisas dentro da pasta de saída
    $_.FullName -notmatch ([Regex]::Escape("\ExportTxt\"))
  } |
  ForEach-Object {
    # Caminho relativo da pasta do arquivo em relação ao BaseDir (remove .\)
    $relDir = Resolve-Path -LiteralPath $_.DirectoryName -Relative
    $relDir = $relDir.TrimStart('.\')

    # Monta destino espelhando a estrutura
    $dstDir = Join-Path $OutDir $relDir
    if (-not (Test-Path -LiteralPath $dstDir)) {
      New-Item -ItemType Directory -Path $dstDir | Out-Null
    }

    # Exporta conteúdo do .py para .txt com mesmo nome-base
    $dst = Join-Path $dstDir ($_.BaseName + '.txt')
    $content = Get-Content -LiteralPath $_.FullName -Raw
    Set-Content -LiteralPath $dst -Value $content -Encoding utf8

    Write-Host "[OK]" $_.FullName '>' $dst
  }

Write-Host "[INFO] Concluído."

