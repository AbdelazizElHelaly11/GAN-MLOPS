"""
Generate a PDF report documenting YAML bugs and fixes for the GitHub Actions ML Pipeline
"""
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

# Create PDF
pdf_path = "YAML_Bug_Report.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
styles = getSampleStyleSheet()
elements = []

# Title
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#1f4788'),
    spaceAfter=30,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)
elements.append(Paragraph("GitHub Actions ML Pipeline", title_style))
elements.append(Paragraph("YAML Bug Report & Implementation", title_style))
elements.append(Spacer(1, 0.3*inch))

# Document info
info_style = ParagraphStyle(
    'Info',
    parent=styles['Normal'],
    fontSize=10,
    textColor=colors.grey,
    alignment=TA_CENTER
)
elements.append(Paragraph(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", info_style))
elements.append(Paragraph("GAN Project - MLOps Assignment", info_style))
elements.append(Spacer(1, 0.3*inch))

# Executive Summary
heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#1f4788'),
    spaceAfter=12,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)
elements.append(Paragraph("Executive Summary", heading_style))
summary_text = """
The original GitHub Actions workflow YAML file contained 6 critical bugs that prevented proper execution. 
This report identifies each bug, explains its impact, and documents the solution implemented. 
All bugs have been fixed and the corrected workflow has been successfully deployed and tested.
"""
elements.append(Paragraph(summary_text, styles['Normal']))
elements.append(Spacer(1, 0.2*inch))

# Bug Details Table Header
elements.append(Paragraph("Identified Bugs", heading_style))

# Bug 1
elements.append(Paragraph("<b>Bug #1: Incorrect YAML Syntax - Missing proper indentation for 'on:' trigger</b>", styles['Heading3']))
bug1_data = [
    ["Issue", "The 'on:' trigger block was not properly indented, causing YAML parser errors."],
    ["Original Code", "on:\npush:\nbranches: main"],
    ["Problem", "YAML requires consistent indentation. The 'push:' key should be indented under 'on:', and 'branches:' should be indented under 'push:'."],
    ["Fixed Code", "on:\n  push:\n    branches:\n      - '**'\n      - '!main'"],
    ["Impact", "Critical - Workflow file would not parse correctly."],
]
bug1_table = Table(bug1_data, colWidths=[1.2*inch, 3.8*inch])
bug1_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0f8')),
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
]))
elements.append(bug1_table)
elements.append(Spacer(1, 0.15*inch))

# Bug 2
elements.append(Paragraph("<b>Bug #2: Missing 'uses' attribute for actions</b>", styles['Heading3']))
bug2_data = [
    ["Issue", "The 'Set up Python' step had no 'uses:' attribute referencing the actual GitHub Action."],
    ["Original Code", "- name: Set up Python\nwith:\n  python-version: '3.10'"],
    ["Problem", "GitHub Actions require a 'uses:' key to specify which action to run. Without it, the step cannot execute."],
    ["Fixed Code", "- name: Set up Python\n  uses: actions/setup-python@v5\n  with:\n    python-version: '3.10'"],
    ["Impact", "Critical - Step would fail immediately with 'Missing required attribute' error."],
]
bug2_table = Table(bug2_data, colWidths=[1.2*inch, 3.8*inch])
bug2_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0f8')),
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
]))
elements.append(bug2_table)
elements.append(Spacer(1, 0.15*inch))

# Bug 3
elements.append(Paragraph("<b>Bug #3: Incomplete step - 'Linter Check' with no command</b>", styles['Heading3']))
bug3_data = [
    ["Issue", "The 'Linter Check' step has a name but no 'run:' command specified."],
    ["Original Code", "- name: Linter Check"],
    ["Problem", "Each step must have either a 'uses:' (for actions) or 'run:' (for shell commands). Without either, the step is incomplete."],
    ["Fixed Code", "- name: Linter Check\n  run: python -m py_compile StudentA.py"],
    ["Impact", "Critical - Workflow validation would fail due to incomplete step definition."],
]
bug3_table = Table(bug3_data, colWidths=[1.2*inch, 3.8*inch])
bug3_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0f8')),
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
]))
elements.append(bug3_table)
elements.append(Spacer(1, 0.15*inch))

# Bug 4
elements.append(Paragraph("<b>Bug #4: Missing 'Checkout Code' step</b>", styles['Heading3']))
bug4_data = [
    ["Issue", "The workflow did not include a step to check out the repository code."],
    ["Original Code", "None - step was missing"],
    ["Problem", "Without checking out the code first, subsequent steps cannot access the repository files (requirements.txt, StudentA.py, etc.)."],
    ["Fixed Code", "- name: Checkout Code\n  uses: actions/checkout@v4"],
    ["Impact", "Critical - All subsequent steps would fail as they have no access to project files."],
]
bug4_table = Table(bug4_data, colWidths=[1.2*inch, 3.8*inch])
bug4_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0f8')),
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
]))
elements.append(bug4_table)
elements.append(Spacer(1, 0.15*inch))

# Bug 5
elements.append(Paragraph("<b>Bug #5: Trigger configuration runs on main branch</b>", styles['Heading3']))
bug5_data = [
    ["Issue", "The 'on.push.branches' was set to 'main', but requirements specified running on all branches EXCEPT main."],
    ["Original Code", "on:\n  push:\n    branches: main"],
    ["Problem", "The requirement was to trigger on every push for all branches except main. The original only runs on main, which is the opposite."],
    ["Fixed Code", "on:\n  push:\n    branches:\n      - '**'\n      - '!main'"],
    ["Impact", "High - Does not meet requirements; pipeline won't run on feature branches where it's needed most."],
]
bug5_table = Table(bug5_data, colWidths=[1.2*inch, 3.8*inch])
bug5_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0f8')),
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
]))
elements.append(bug5_table)
elements.append(Spacer(1, 0.15*inch))

# Bug 6
elements.append(Paragraph("<b>Bug #6: Missing artifact upload step</b>", styles['Heading3']))
bug6_data = [
    ["Issue", "No step to upload the README.md as a GitHub artifact named 'project-doc'."],
    ["Original Code", "None - step was missing"],
    ["Problem", "The assignment requires uploading the project's README.md as an artifact. This functionality was entirely missing."],
    ["Fixed Code", "- name: Upload Project Documentation\n  uses: actions/upload-artifact@v4\n  with:\n    name: project-doc\n    path: README.md"],
    ["Impact", "High - Fails to meet artifact upload requirement of the assignment."],
]
bug6_table = Table(bug6_data, colWidths=[1.2*inch, 3.8*inch])
bug6_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0f8')),
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
]))
elements.append(bug6_table)
elements.append(Spacer(1, 0.2*inch))

# Summary Table
elements.append(Paragraph("Bug Summary", heading_style))
summary_table_data = [
    ["Bug #", "Category", "Severity", "Status"],
    ["1", "YAML Indentation", "Critical", "✓ Fixed"],
    ["2", "Missing Action Reference", "Critical", "✓ Fixed"],
    ["3", "Incomplete Step", "Critical", "✓ Fixed"],
    ["4", "Missing Required Step", "Critical", "✓ Fixed"],
    ["5", "Wrong Trigger Logic", "High", "✓ Fixed"],
    ["6", "Missing Feature", "High", "✓ Fixed"],
]
summary_table = Table(summary_table_data, colWidths=[0.8*inch, 1.8*inch, 1.2*inch, 1.2*inch])
summary_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 11),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
]))
elements.append(summary_table)
elements.append(Spacer(1, 0.3*inch))

# Implementation Details
elements.append(Paragraph("Implementation Details", heading_style))
elements.append(Paragraph("<b>Final Corrected Workflow Structure:</b>", styles['Heading3']))

impl_text = """
The corrected workflow includes:
<br/><br/>
<b>1. Triggers (on:)</b>
<br/>
• Runs on: All branches except main (- '**' and - '!main')
<br/>
• Also runs on: All pull requests
<br/><br/>

<b>2. Job Steps (validate-and-test):</b>
<br/>
• Checkout Code: Uses actions/checkout@v4
<br/>
• Set up Python: Uses actions/setup-python@v5 with version 3.10
<br/>
• Install Dependencies: Runs pip install -r requirements.txt
<br/>
• Linter Check: Compiles StudentA.py using python -m py_compile
<br/>
• Model Dry Test: Tests torch import and environment readiness
<br/>
• Upload Project Documentation: Uploads README.md as 'project-doc' artifact
<br/><br/>

<b>3. Key Improvements:</b>
<br/>
• All YAML syntax is properly formatted and valid
<br/>
• Each step has required attributes (name, uses/run, with if needed)
<br/>
• Trigger logic correctly excludes main branch
<br/>
• Includes all necessary actions from GitHub Marketplace
<br/>
• Implements artifact upload as required
"""
elements.append(Paragraph(impl_text, styles['Normal']))
elements.append(Spacer(1, 0.2*inch))

# File Locations
elements.append(Paragraph("Repository Information", heading_style))
repo_text = """
<b>Repository:</b> AbdelazizElHelaly11/YOLO_ObjectTraking
<br/>
<b>Workflow File:</b> .github/workflows/ml-pipeline.yml
<br/>
<b>Documentation:</b> README.md (created as part of this assignment)
<br/>
<b>GitHub Actions URL:</b> https://github.com/AbdelazizElHelaly11/YOLO_ObjectTraking/actions
"""
elements.append(Paragraph(repo_text, styles['Normal']))
elements.append(Spacer(1, 0.3*inch))

# Conclusion
elements.append(Paragraph("Conclusion", heading_style))
conclusion_text = """
All 6 identified bugs in the original GitHub Actions workflow YAML file have been successfully fixed. 
The corrected workflow file is now validated, properly formatted, and deployed to the repository. 
The pipeline successfully implements all required features including:
<br/><br/>
✓ Proper YAML syntax and indentation
<br/>
✓ Correct trigger configuration (all branches except main)
<br/>
✓ All necessary steps with proper action references
<br/>
✓ Artifact upload functionality for README.md
<br/>
✓ Python environment setup and dependency installation
<br/>
✓ Code validation and model testing
<br/><br/>

The workflow is now ready for automated validation and testing on every push to feature branches and pull requests.
"""
elements.append(Paragraph(conclusion_text, styles['Normal']))

# Build PDF
doc.build(elements)
print(f"✓ PDF Report generated successfully: {pdf_path}")
