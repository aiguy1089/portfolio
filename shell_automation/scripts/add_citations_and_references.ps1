Param(
    [string]$DocPath = "c:\Users\Admin\D796\Project Submission\Combined_Project_Submission.docx"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $DocPath)) {
    Write-Error "Document not found: $DocPath"
    exit 1
}

# Open Word
try {
    $word = New-Object -ComObject Word.Application
} catch {
    Write-Error "Microsoft Word is required. COM object could not be created. $_"
    exit 1
}
$word.Visible = $false

$doc = $word.Documents.Open($DocPath)
$selection = $word.Selection

function InsertAfterHeading {
    param(
        [string]$headingText,
        [string]$citationText
    )
    # Search for the Heading 1 paragraph with exact text and insert a paragraph after it with the provided citation text
    $range = $doc.Content
    $find = $range.Find
    $find.ClearFormatting()
    $find.Text = $headingText
    $find.Forward = $true
    $find.Wrap = 1 # wdFindContinue
    if ($find.Execute()) {
        # Move to the end of the found paragraph
        $foundPara = $range.Paragraphs(1)
        $insertRange = $foundPara.Range.Duplicate
        $insertRange.Collapse(0) # wdCollapseEnd
        # Insert a new paragraph and add the citation text
        $insertRange.InsertParagraphAfter() | Out-Null
        $insertRange = $foundPara.Range.Duplicate
        $insertRange.SetRange($foundPara.Range.End, $foundPara.Range.End)
        $insertRange.Text = "($citationText)"
        # Ensure a blank line after
        $afterRange = $insertRange.Duplicate
        $afterRange.Collapse(0) # end
        $afterRange.InsertParagraphAfter() | Out-Null
    } else {
        Write-Warning "Heading not found: $headingText"
    }
}

# In-text citations mapping (exactly the 8 sources total)
# We'll reference relevant ones per section and acknowledge AI tools near the end as well.

# Section-specific citations
InsertAfterHeading -headingText 'Task 1: Creating Shell Scripts' -citationText 'Shotts, 2019; Nemeth et al., 2017; Free Software Foundation, 2024a'
InsertAfterHeading -headingText 'Configuration Guide' -citationText 'Free Software Foundation, 2024a; Ubuntu Manpage, 2024'
InsertAfterHeading -headingText 'Testing Results' -citationText 'Free Software Foundation, 2024b'
InsertAfterHeading -headingText 'Network Flowchart' -citationText 'Postel, 1981'

# Add an acknowledgment paragraph for AI tools before the References
$endRange = $doc.Content.Duplicate
$endRange.Collapse(0) # end
$endRange.InsertParagraphAfter() | Out-Null
$endRange = $doc.Content.Duplicate; $endRange.Collapse(0)
$endRange.Text = "Acknowledgment: Outline and drafting assistance was provided by AI tools (OpenAI, 2025a; OpenAI, 2025b)."
$endRange = $doc.Content.Duplicate; $endRange.Collapse(0); $endRange.InsertParagraphAfter() | Out-Null

# Add References section
$refsHeading = $doc.Content.Duplicate; $refsHeading.Collapse(0)
$refsHeading.InsertParagraphAfter() | Out-Null
$refsHeading = $doc.Content.Duplicate; $refsHeading.Collapse(0)
$refsHeading.Text = "References"
# Apply Heading 1 style to the heading if available
try { $refsHeading.Style = 'Heading 1' } catch {}

# References list (exactly eight entries)
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

foreach ($ref in $references) {
    $r = $doc.Content.Duplicate; $r.Collapse(0)
    $r.InsertParagraphAfter() | Out-Null
    $r = $doc.Content.Duplicate; $r.Collapse(0)
    $r.Text = $ref
}

# Update TOC again in case headings changed
foreach ($toc in $doc.TablesOfContents) { $toc.Update() }

# Save and close
$doc.Save()
$doc.Close($false)
$word.Quit()

# Release COM objects
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($selection) | Out-Null
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($doc) | Out-Null
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
[GC]::Collect(); [GC]::WaitForPendingFinalizers()

Write-Host "Citations and References inserted successfully."