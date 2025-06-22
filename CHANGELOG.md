# Changelog

All notable changes to this project will be documented in this file.

---

## 0.1.0-alpha – 22/06/25

### Added
- `converter.py`: Initial PageScript to HTML converter supporting:
  - Headings (`#`)
  - Paragraphs
  - Bold (`**text**`) and italic (`*text*`)
  - Images `[image: src]`
  - Buttons `[button: text > link]`
  - Links `[link: text > url]`
  - Horizontal rule (`---`)
- `README.md`: Project overview and How-To guide
- `syntax.txt`: Examples of every supported PageScript element
- `LICENSE.md`: MIT License

---

## 0.1.1-alpha - 22/06/25

### Fixed
- `converter.py`: Fixed triple quote marks

---

## 0.1.2-alpha - 22/06/25

### Added
- PageScript:
  - `[Title: ...]`: Sets the `<title>` tag in the HTML `<head>`
  - `[Favicon: ...]`: Inserts a favicon using `<link rel="icon">`
  - `[List: item1 | item2 | ...]`: Unordered lists rendered as `<ul><li>...</li></ul>`
  - `[OList: item1 | item2 | ...]`: Ordered lists rendered as `<ol><li>...</li></ol>`
  - `[Table: ... ]`: Pipe-separated table block ending with `]`, rendered as `<table>`
  - `[Script: ... ]`: Raw JavaScript inside `<script>` tags, also block-ended with `]`
- Other:
  - Added `example.pagescript`

### Changed
- Refactored `converter.py` to generate full HTML document structure (`<!DOCTYPE html>`, `<html>`, `<head>`, `<body>`)
- Internal logic updated to group head metadata separately from content rendering

### Fixed
- Minor spacing and formatting tweaks for output consistency
