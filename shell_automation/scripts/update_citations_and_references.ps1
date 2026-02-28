Param(
    [string]$DocPath = "c:\Users\Admin\D796\Project Submission\Combined_Project_Submission.docx"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $DocPath)) {
    Write-Error "Document not found: $DocPath"
    exit 1
}

function New-WordApp {
    try { return New-Object -ComObject Word.Application } catch { throw "Microsoft Word is required. $_" }
}

$word = New-WordApp
$word.Visible = $false
$doc = $word.Documents.Open($DocPath)

# Try to unprotect the document if protection is enabled
try {
    if ($doc.ProtectionType -ne -1) {  # -1 == wdNoProtection
        $doc.Unprotect() | Out-Null
    }
} catch { Write-Warning "Could not unprotect document. $_" }

# Helper: append citations to the end of the first paragraph after a given Heading 1
function MoveCitationsToFirstParagraphAfterHeading {
    param(
        [Parameter(Mandatory=$true)][string]$HeadingText,
        [Parameter(Mandatory=$true)][string]$CitationText,
        [string[]]$KnownCiteMarkers
    )
    $range = $doc.Content
    $find = $range.Find
    $find.ClearFormatting()
    $find.Text = $HeadingText
    $find.Forward = $true
    $find.Wrap = 1 # wdFindContinue

    if (-not $find.Execute()) { Write-Warning "Heading not found: $HeadingText"; return }

    # Create a range after the heading
    $postRange = $doc.Range($range.End, $doc.Content.End)

    if ($postRange.Paragraphs.Count -eq 0) { return }

    # If the first paragraph after heading contains our previous parentheses-only citation, remove it
    $firstPara = $postRange.Paragraphs(1)
    $firstText = ($firstPara.Range.Text -replace "\r", "").Trim()
    $hasKnown = $false
    foreach ($m in $KnownCiteMarkers) { if ($firstText -like ("*${m}*")) { $hasKnown = $true; break } }
    if ($firstText.StartsWith("(") -and $hasKnown) {
        $firstPara.Range.Delete()
        # Recompute first paragraph after deletion
        $postRange = $doc.Range($range.End, $doc.Content.End)
        if ($postRange.Paragraphs.Count -eq 0) { return }
        $firstPara = $postRange.Paragraphs(1)
    }

    # Append the citation to the end of the first paragraph (before the paragraph mark)
    $appendRange = $doc.Range($firstPara.Range.End - 1, $firstPara.Range.End - 1)
    $textBefore = (($firstPara.Range.Text) -replace "\r", "").Trim()
    $space = if ($textBefore -match "[\w\)]$") { " " } else { "" }
    $appendRange.Text = "$space($CitationText)"
}

# Apply moves with our 4 section mappings
MoveCitationsToFirstParagraphAfterHeading -HeadingText 'Task 1: Creating Shell Scripts' -CitationText 'Shotts, 2019; Nemeth et al., 2017; Free Software Foundation, 2024a' -KnownCiteMarkers @('Shotts','Nemeth','Free Software Foundation')
MoveCitationsToFirstParagraphAfterHeading -HeadingText 'Configuration Guide' -CitationText 'Free Software Foundation, 2024a; Ubuntu Manpage, 2024' -KnownCiteMarkers @('Free Software Foundation','Ubuntu Manpage')
MoveCitationsToFirstParagraphAfterHeading -HeadingText 'Testing Results' -CitationText 'Free Software Foundation, 2024b' -KnownCiteMarkers @('Free Software Foundation')
MoveCitationsToFirstParagraphAfterHeading -HeadingText 'Network Flowchart' -CitationText 'Postel, 1981' -KnownCiteMarkers @('Postel')

# Attempt to remove any existing References section to avoid duplicates
try {
    $rngRef = $doc.Content
    $findRef = $rngRef.Find
    $findRef.ClearFormatting(); $findRef.Text = 'References'; $findRef.Forward = $true; $findRef.Wrap = 1
    if ($findRef.Execute()) {
        $start = $rngRef.Start
        $delRange = $doc.Range($start, $doc.Content.End)
        $delRange.Delete()
    }
} catch {
    Write-Warning "Could not remove existing References section. A new section will be appended. $_"
}

# Also remove any existing previous acknowledgment line (best-effort)
try {
    $rngAck = $doc.Content; $fdAck = $rngAck.Find
    $fdAck.ClearFormatting(); $fdAck.Text = 'Acknowledgment: Outline and drafting assistance'; $fdAck.Forward = $true; $fdAck.Wrap = 1
    while ($fdAck.Execute()) { $rngAck.Paragraphs(1).Range.Delete(); $rngAck = $doc.Content; $fdAck = $rngAck.Find; $fdAck.ClearFormatting(); $fdAck.Text = 'Acknowledgment: Outline and drafting assistance'; $fdAck.Forward = $true; $fdAck.Wrap = 1 }
} catch { Write-Warning "Could not clean previous acknowledgment lines. $_" }

# Insert acknowledgment paragraph near end
$endRange = $doc.Content.Duplicate; $endRange.Collapse(0)
$endRange.InsertParagraphAfter() | Out-Null
$endRange = $doc.Content.Duplicate; $endRange.Collapse(0)
$endRange.Text = 'Acknowledgment: Outline and drafting assistance was provided by AI tools (OpenAI, 2025a; OpenAI, 2025b).'
$endRange = $doc.Content.Duplicate; $endRange.Collapse(0); $endRange.InsertParagraphAfter() | Out-Null

# Insert References heading
$refsHeading = $doc.Content.Duplicate; $refsHeading.Collapse(0)
$refsHeading.InsertParagraphAfter() | Out-Null
$refsHeading = $doc.Content.Duplicate; $refsHeading.Collapse(0)
$refsHeading.Text = 'References'
try { $refsHeading.Style = 'Heading 1' } catch {}

# References list (exactly eight entries, alphabetized by author)
$references = @(
    'Free Software Foundation. (2024a). Bash reference manual (Version 5.2). https://www.gnu.org/software/bash/manual/',
    'Free Software Foundation. (2024b). GNU coreutils manual. https://www.gnu.org/software/coreutils/manual/',
    'Nemeth, E., Snyder, T. R., Hein, G., Whaley, B., & Mackin, D. (2017). UNIX and Linux system administration handbook (5th ed.). Addison-Wesley Professional.',
    'OpenAI. (2025a). ChatGPT (o-series) [Large language model]. https://chat.openai.com/',
    'OpenAI. (2025b). Zencoder (GPT-5 o-series) [Large language model]. https://openai.com/',
    'Postel, J. (1981). Internet control message protocol (RFC 792). Internet Engineering Task Force. https://www.rfc-editor.org/rfc/rfc792',
    'Shotts, W. E., Jr. (2019). The Linux command line (2nd ed.). No Starch Press. https://linuxcommand.org/tlcl.php',
    'Ubuntu Manpage. (2024). apt(8) – Advanced Package Tool. https://manpages.ubuntu.com/manpages/noble/en/man8/apt.8.html'
)

# Helper: apply hanging indent to a paragraph range
function ApplyHangingIndent($paraRange) {
    $paraRange.ParagraphFormat.LeftIndent = 36  # 0.5 inch
    $paraRange.ParagraphFormat.FirstLineIndent = -36
}

# Helper: italicize substring within a range if found
function ItalicizeSubstring($paraRange, $substring) {
    $sub = $paraRange.Duplicate
    $fd = $sub.Find
    $fd.ClearFormatting(); $fd.Text = $substring; $fd.Forward = $true; $fd.Wrap = 0
    if ($fd.Execute()) { $sub.Font.Italic = $true }
}

foreach ($ref in $references) {
    $r = $doc.Content.Duplicate; $r.Collapse(0)
    $r.InsertParagraphAfter() | Out-Null
    $r = $doc.Content.Duplicate; $r.Collapse(0)
    $r.Text = $ref
    ApplyHangingIndent -paraRange $r
    # Italicize book titles where applicable
    ItalicizeSubstring -paraRange $r -substring 'UNIX and Linux system administration handbook'
    ItalicizeSubstring -paraRange $r -substring 'The Linux command line'
}

# Update TOC
foreach ($toc in $doc.TablesOfContents) { $toc.Update() }

# Save and close
$doc.Save()
$doc.Close($false)
$word.Quit()

# Cleanup
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($doc) | Out-Null
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
[GC]::Collect(); [GC]::WaitForPendingFinalizers()

Write-Host 'Citations moved and References formatted per APA 7.'