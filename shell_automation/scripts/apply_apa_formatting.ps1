Param(
    [string]$DocPath = "c:\Users\Admin\D796\Project Submission\Combined_Project_Submission.docx"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $DocPath)) {
    Write-Error "Document not found: $DocPath"
    exit 1
}

# Clear file read-only attribute (best effort)
try {
    $file = Get-Item -LiteralPath $DocPath
    if ($file.Attributes -band [IO.FileAttributes]::ReadOnly) {
        $file.Attributes = $file.Attributes -bxor [IO.FileAttributes]::ReadOnly
    }
    # Also try attrib to be safe
    cmd /c attrib -R "$DocPath" | Out-Null
} catch { Write-Warning "Could not clear file read-only attribute. $_" }

function New-WordApp { try { return New-Object -ComObject Word.Application } catch { throw "Microsoft Word is required. $_" } }

$word = New-WordApp
$word.Visible = $false
$word.DisplayAlerts = 0

# Open as editable (ReadOnly = $false)
$doc = $word.Documents.Open($DocPath, $false, $false)
$doc.Activate()

# Try to unprotect, best effort
try { if ($doc.ProtectionType -ne -1) { $doc.Unprotect() | Out-Null } } catch { Write-Warning "Document might be protected; proceeding with accessible parts. $_" }

# Locate the 'References' heading
$rng = $doc.Content
$f = $rng.Find
$f.ClearFormatting(); $f.Text = 'References'; $f.Forward = $true; $f.Wrap = 1
if (-not $f.Execute()) { Write-Error "References heading not found." }

# Range after the heading
$afterRef = $doc.Range($rng.End, $doc.Content.End)

# Target exactly our 8 known references
$starts = @(
    'Free Software Foundation. (2024a). Bash reference manual',
    'Free Software Foundation. (2024b). GNU coreutils manual',
    'Nemeth, E., Snyder, T. R., Hein, G., Whaley, B., & Mackin, D. (2017).',
    'OpenAI. (2025a). ChatGPT (o-series)',
    'OpenAI. (2025b). Zencoder (GPT-5 o-series)',
    'Postel, J. (1981). Internet control message protocol',
    'Shotts, W. E., Jr. (2019). The Linux command line',
    'Ubuntu Manpage. (2024). apt(8) – Advanced Package Tool'
)

function ApplyHangingIndent($paraRange) {
    $paraRange.ParagraphFormat.LeftIndent = 36  # 0.5 inch
    $paraRange.ParagraphFormat.FirstLineIndent = -36
    $paraRange.ParagraphFormat.SpaceBefore = 0
    $paraRange.ParagraphFormat.SpaceAfter = 0
    $paraRange.ParagraphFormat.LineSpacingRule = 1  # wdLineSpaceSingle
}

function ItalicizeSubstring($paraRange, $substring) {
    $sub = $paraRange.Duplicate
    $fd = $sub.Find
    $fd.ClearFormatting(); $fd.Text = $substring; $fd.Forward = $true; $fd.Wrap = 0
    if ($fd.Execute()) { $sub.Font.Italic = $true }
}

# Format lines
for ($i = 1; $i -le $afterRef.Paragraphs.Count; $i++) {
    $p = $afterRef.Paragraphs($i)
    $text = ($p.Range.Text -replace "\r", "").Trim()
    if (-not $text) { continue }
    foreach ($s in $starts) {
        if ($text.StartsWith($s)) {
            ApplyHangingIndent -paraRange $p.Range
            ItalicizeSubstring -paraRange $p.Range -substring 'UNIX and Linux system administration handbook'
            ItalicizeSubstring -paraRange $p.Range -substring 'The Linux command line'
            break
        }
    }
}

# Ensure the 'References' heading uses Heading 1
try {
    $hdrRange = $doc.Content; $fh = $hdrRange.Find; $fh.ClearFormatting(); $fh.Text = 'References'; $fh.Forward = $true; $fh.Wrap = 1
    if ($fh.Execute()) { $hdrRange.Paragraphs(1).Range.Style = 'Heading 1' }
} catch {}

# Save and close
$doc.Save()
$doc.Close($false)
$word.Quit()

[System.Runtime.Interopservices.Marshal]::ReleaseComObject($doc) | Out-Null
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
[GC]::Collect(); [GC]::WaitForPendingFinalizers()

Write-Host 'APA formatting applied to References (hanging indent, spacing, italics for book titles).'