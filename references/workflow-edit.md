# Workflow: Edit Existing PPTX (XML Unpack/Edit/Repack)

## Pipeline Overview

```
Template PPTX → Analyze → Unpack → Structural Changes → Edit Content → Clean → Validate → Repack
```

## Step 1: Analyze Template

```bash
python scripts/thumbnail.py template.pptx
python -m markitdown template.pptx
```

- `thumbnails.jpg`: Visual grid of slides with filenames as labels
- markitdown output: Extracted text content

Use thumbnails to identify layout types and map content to slides.

## Step 2: Plan Slide Mapping

For each content section, choose a template slide.

**Use varied layouts** — monotonous presentations are the #1 failure mode:
- Multi-column layouts (2-column, 3-column)
- Image + text combinations
- Full-bleed images with text overlay
- Quote or callout slides
- Section dividers
- Stat/number callouts
- Icon grids or icon + text rows

**Avoid**: Repeating the same text-heavy layout for every slide.

Match content type to layout style:
- Key points → bullet slide
- Team info → multi-column
- Testimonials → quote slide
- Data → chart/number callout

## Step 3: Unpack

```bash
python scripts/office/unpack.py template.pptx unpacked/
```

What this does:
1. Extracts the PPTX ZIP archive
2. Pretty-prints all XML files (2-space indent for readability)
3. Escapes smart quotes (`""''` → XML entities like `&#x201C;`)

Output: `unpacked/` directory with readable XML files.

## Step 4: Structural Changes (Sequential — NOT with subagents)

Do all structural changes yourself before editing content:

### Delete slides
Remove `<p:sldId>` from `<p:sldIdLst>` in `ppt/presentation.xml`.

### Duplicate slides
```bash
python scripts/add_slide.py unpacked/ slide2.xml
```
Prints `<p:sldId>` to paste into `presentation.xml`.

### Create from layout
```bash
python scripts/add_slide.py unpacked/ slideLayout2.xml
```

### Reorder slides
Rearrange `<p:sldId>` elements in `<p:sldIdLst>`.

**Important**: Never manually copy slide files. `add_slide.py` handles:
- Content_Types.xml updates
- presentation.xml.rels relationships
- Slide ID generation
- Notes slide reference cleanup

## Step 5: Edit Content (Parallelizable with subagents)

Each slide is a separate XML file: `ppt/slides/slide{N}.xml`.

### Using subagents

In your prompt to subagents, include:
- The slide file path(s) to edit
- "Use the Edit tool for all changes"
- The formatting rules below

### Content editing process

For each slide:
1. Read the slide's XML
2. Identify ALL placeholder content — text, images, charts, icons, captions
3. Replace each placeholder with final content

### Formatting Rules

- **Bold headers**: `b="1"` on `<a:rPr>` for titles, section headers, inline labels
- **Never use unicode bullets**: Use `<a:buChar>` or `<a:buAutoNum>`
- **Bullet consistency**: Let bullets inherit from layout
- **Multi-item content**: Separate `<a:p>` elements, never concatenate into one string

### Multi-item content pattern

```xml
<!-- CORRECT: Separate paragraphs with bold headers -->
<a:p>
  <a:pPr algn="l"><a:lnSpc><a:spcPts val="3919"/></a:lnSpc></a:pPr>
  <a:r><a:rPr lang="en-US" sz="2799" b="1"/><a:t>Step 1</a:t></a:r>
</a:p>
<a:p>
  <a:pPr algn="l"><a:lnSpc><a:spcPts val="3919"/></a:lnSpc></a:pPr>
  <a:r><a:rPr lang="en-US" sz="2799"/><a:t>Do the first thing.</a:t></a:r>
</a:p>

<!-- WRONG: All items in one paragraph -->
<a:p>
  <a:r><a:rPr .../><a:t>Step 1: Do the first thing. Step 2: Do the second thing.</a:t></a:r>
</a:p>
```

### Smart Quotes

Handled automatically by unpack/pack. When adding new text with quotes, use XML entities:

| Character | Entity |
|-----------|--------|
| `"` (left double) | `&#x201C;` |
| `"` (right double) | `&#x201D;` |
| `'` (left single) | `&#x2018;` |
| `'` (right single) | `&#x2019;` |

## Step 6: Clean & Validate

```bash
python scripts/clean.py unpacked/
```

Removes:
- Orphaned slides (not in sldIdLst)
- Unreferenced media, embeddings, charts
- Orphaned .rels files
- [trash] directory
- Content-Type overrides for deleted files

## Step 7: Pack

```bash
python scripts/office/pack.py unpacked/ output.pptx --original template.pptx
```

What this does:
1. Runs XSD schema validation with auto-repair
2. Condenses XML (removes whitespace, comments)
3. Re-encodes smart quotes
4. Creates ZIP with DEFLATED compression

## Common Pitfalls

### Template Adaptation

When source has fewer items than template:
- **Remove excess elements entirely** (images, shapes, text boxes)
- Don't just clear text — check for orphaned visuals
- Run visual QA to catch mismatched counts

When replacing text with different length:
- Shorter: Usually safe
- Longer: May overflow — test with visual QA

### Template slots ≠ Source items

If template has 4 team members but source has 3:
- Delete the 4th member's ENTIRE group (image + text boxes)
- Don't just clear the text

### XML Parsing

- **Use** `defusedxml.minidom` — safe, preserves namespaces
- **Never use** `xml.etree.ElementTree` — corrupts namespaces

### Whitespace

Use `xml:space="preserve"` on `<a:t>` with leading/trailing spaces.
