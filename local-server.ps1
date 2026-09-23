param(
  [ValidateRange(1024, 65535)]
  [int]$Port = 8787,
  [switch]$NoBrowser
)

$ErrorActionPreference = "Stop"
$Root = [System.IO.Path]::GetFullPath($PSScriptRoot)
$RootPrefix = $Root.TrimEnd([System.IO.Path]::DirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar
$Prefix = "http://127.0.0.1:$Port/"
$Mime = @{
  ".html" = "text/html; charset=utf-8"
  ".js" = "text/javascript; charset=utf-8"
  ".mjs" = "text/javascript; charset=utf-8"
  ".css" = "text/css; charset=utf-8"
  ".json" = "application/json; charset=utf-8"
  ".webmanifest" = "application/manifest+json"
  ".svg" = "image/svg+xml"
  ".wasm" = "application/wasm"
  ".txt" = "text/plain; charset=utf-8"
  ".md" = "text/markdown; charset=utf-8"
  ".gz" = "application/gzip"
}

function Send-Headers($Stream, [int]$Status, [string]$Reason, [string]$ContentType, [long]$Length) {
  $Headers = "HTTP/1.1 $Status $Reason`r`n" +
    "Content-Type: $ContentType`r`n" +
    "Content-Length: $Length`r`n" +
    "Cache-Control: no-cache`r`n" +
    "X-Content-Type-Options: nosniff`r`n" +
    "Cross-Origin-Opener-Policy: same-origin`r`n" +
    "Cross-Origin-Embedder-Policy: require-corp`r`n" +
    "Content-Security-Policy: default-src 'self'; script-src 'self' 'wasm-unsafe-eval'; worker-src 'self' blob:; style-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'`r`n" +
    "Connection: close`r`n`r`n"
  $Bytes = [System.Text.Encoding]::ASCII.GetBytes($Headers)
  $Stream.Write($Bytes, 0, $Bytes.Length)
}

function Send-Text($Stream, [int]$Status, [string]$Reason, [string]$Message, [bool]$HeadOnly) {
  $Body = [System.Text.Encoding]::UTF8.GetBytes($Message)
  Send-Headers $Stream $Status $Reason "text/plain; charset=utf-8" $Body.Length
  if (-not $HeadOnly) { $Stream.Write($Body, 0, $Body.Length) }
}

$Listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, $Port)
try {
  $Listener.Start()
  Write-Host "plusultra: $Prefix"
  Write-Host "Press Ctrl+C to stop the server."
  if (-not $NoBrowser) { Start-Process $Prefix }

  while ($true) {
    $Client = $Listener.AcceptTcpClient()
    try {
      $Client.NoDelay = $true
      $Stream = $Client.GetStream()
      $Reader = [System.IO.StreamReader]::new($Stream, [System.Text.Encoding]::ASCII, $false, 8192, $true)
      $RequestLine = $Reader.ReadLine()
      while (($Header = $Reader.ReadLine()) -ne $null -and $Header -ne "") {}
      if ([string]::IsNullOrWhiteSpace($RequestLine)) { continue }

      $Parts = $RequestLine.Split(' ')
      if ($Parts.Length -lt 3) { Send-Text $Stream 400 "Bad Request" "Invalid request." $false; continue }
      $Method = $Parts[0].ToUpperInvariant()
      $HeadOnly = $Method -eq "HEAD"
      if ($Method -ne "GET" -and -not $HeadOnly) { Send-Text $Stream 405 "Method Not Allowed" "Method not allowed." $false; continue }

      $RequestUri = [System.Uri]::new("http://127.0.0.1" + $Parts[1])
      $Relative = [System.Uri]::UnescapeDataString($RequestUri.AbsolutePath).TrimStart('/')
      if ([string]::IsNullOrWhiteSpace($Relative)) { $Relative = "index.html" }
      $Relative = $Relative.Replace('/', [System.IO.Path]::DirectorySeparatorChar)
      $Target = [System.IO.Path]::GetFullPath([System.IO.Path]::Combine($Root, $Relative))
      if (-not $Target.StartsWith($RootPrefix, [System.StringComparison]::OrdinalIgnoreCase) -or -not [System.IO.File]::Exists($Target)) {
        Send-Text $Stream 404 "Not Found" "Not found." $HeadOnly
        continue
      }

      $Extension = [System.IO.Path]::GetExtension($Target).ToLowerInvariant()
      $ContentType = if ($Mime.ContainsKey($Extension)) { $Mime[$Extension] } else { "application/octet-stream" }
      $Length = (Get-Item -LiteralPath $Target).Length
      Send-Headers $Stream 200 "OK" $ContentType $Length
      if (-not $HeadOnly) {
        $Input = [System.IO.File]::OpenRead($Target)
        try { $Input.CopyTo($Stream) } finally { $Input.Dispose() }
      }
    } catch {
      try { Send-Text $Stream 500 "Internal Server Error" "The file could not be served." $false } catch {}
    } finally {
      if ($null -ne $Reader) { $Reader.Dispose() }
      if ($null -ne $Stream) { $Stream.Dispose() }
      $Client.Dispose()
      $Reader = $null
      $Stream = $null
    }
  }
} catch {
  Write-Error "Could not start $Prefix $($_.Exception.Message)"
  exit 1
} finally {
  $Listener.Stop()
}
