# Changelog

All notable changes to this project will be documented in this file.

---

## [0.1.0-alpha] – 22/06/25

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

## [0.1.1-alpha] - 22/06/25

### Fixed
- `converter.py`: Fixed triple quote marks
