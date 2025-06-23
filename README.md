# PageScript 0.1.3-alpha

**PageScript** is a simplified markup language designed to make web page creation intuitive, clean, and beginner-friendly. With minimal syntax and human-readable commands, it transforms basic text into fully functional HTML — no tangled tags, no coding experience required.

Whether you're a first-time web builder, a teacher introducing web concepts, or a developer who just wants to prototype fast, PageScript offers a refreshing alternative to traditional HTML.

---

## Installation

Install from [PyPI](https://pypi.org/project/pagescript):

```bash
pip install pagescript
```

Or from the latest development version:

```bash
pip install git+https://github.com/CRGSCodingCats/PageScript.git
```

---

## How to Use PageScript

### 1. Write your Markup
Create a plain text file with a `.pagescript` extension using the simple syntax:

```
# Hello, World!

This is a *friendly* and **easy** way to build web pages.

[Image: cat.jpg]

[Button: Click Me > https://example.com]

```
### 2. Run the Converter
Use the Command Prompt or PowerShell:

```bash
pagescript example.pagescript
```

Or, if you're using the script directly:

```bash
python converter.py example.pagescript
```

### 3. Open the Output
It will generate `example.html`. Open that in any browser to view your page.

---

## Example
Explore [`example.pagescript`](https://github.com/CRGSCodingCats/PageScript/blob/main/example.pagescript) to see a sample of what PageScxript can do.

## License
MIT © CRGS Coding Cats MMXXV
