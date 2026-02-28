Param(
    [string]$StudentName = "",
    [string]$Date = ""
)

$ErrorActionPreference = "Stop"

$outputPath = "c:\Users\Admin\D796\Project Submission\Combined_Project_Submission.docx"

try {
    $word = New-Object -ComObject Word.Application
} catch {
    Write-Error "Microsoft Word is required to run this script. COM object could not be created. $_"
    exit 1
}

$word.Visible = $false
$doc = $word.Documents.Add()
$selection = $word.Selection

# -------- Title Page --------
# 1 = Center, 0 = Left
$selection.ParagraphFormat.Alignment = 1
$selection.Font.Size = 20
$selection.Font.Bold = $true
$selection.TypeText('D796 Assessment - Combined Project Submission')
$selection.TypeParagraph(); $selection.TypeParagraph()

$selection.Font.Size = 12
$selection.Font.Bold = $false
if ($StudentName) { $selection.TypeText("Student Name: $StudentName") } else { $selection.TypeText("Student Name: _________________________") }
$selection.TypeParagraph()
if ($Date) { $selection.TypeText("Date: $Date") } else { $selection.TypeText("Date: ___________________") }
$selection.TypeParagraph()
$selection.TypeText("Course: D796 - Unix/Linux System Administration")
$selection.TypeParagraph()

$selection.ParagraphFormat.Alignment = 0

# Insert a new page for Table of Contents
$selection.InsertNewPage()

# -------- Table of Contents --------
$selection.Style = 'Heading 1'
$selection.TypeText('Table of Contents')
$selection.TypeParagraph(); $selection.TypeParagraph()
# Add TOC covering Heading 1..3
[void]$doc.TablesOfContents.Add($selection.Range, $true, 1, 3)

# New page for content
$selection.InsertNewPage()

# -------- Sections to Merge --------
$sections = @(
    @{ Title = 'Task 1: Creating Shell Scripts'; Path = 'c:\Users\Admin\D796\Project Submission\RQN1_Task 1 Creating Shell Scripts.docx' },
    @{ Title = 'Configuration Guide';            Path = 'c:\Users\Admin\D796\Project Submission\Configuration_Guide.docx' },
    @{ Title = 'Testing Results';                Path = 'c:\Users\Admin\D796\Project Submission\Testing_Results.docx' },
    @{ Title = 'Network Flowchart';              Path = 'c:\Users\Admin\D796\Project Submission\Network_Flowchart.docx' }
)

foreach ($s in $sections) {
    if (-not (Test-Path $s.Path)) {
        Write-Warning ('Missing file: ' + $s.Path + ' - skipping this section.')
        continue
    }

    # Section heading
    $selection.Style = 'Heading 1'
    $selection.TypeText($s.Title)
    $selection.TypeParagraph(); $selection.TypeParagraph()

    # Insert the document content
    # InsertFile(FileName, Range, ConfirmConversions, Link, Attachment)
    $selection.InsertFile($s.Path, '', $false, $false, $false)

    # Add a page break after each inserted document
    $selection.TypeParagraph()
    $selection.InsertNewPage()
}

# Update TOC after all content is inserted
foreach ($toc in $doc.TablesOfContents) { $toc.Update() }

# Save and close
$doc.SaveAs([ref]$outputPath)
$doc.Close($false)
$word.Quit()

# Release COM objects
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($selection) | Out-Null
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($doc) | Out-Null
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
[GC]::Collect(); [GC]::WaitForPendingFinalizers()

Write-Host ('Combined document saved to: ' + $outputPath)