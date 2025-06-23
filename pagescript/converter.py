import re
import sys

def extract_attributes(text):
    """
    Extract ID and class attribute tokens from a given text.
    Returns a tuple of (cleaned_text, attributes_string).
    """
    id_match = re.search(r'''

\[id:(.*?)\]

''', text)
    class_match = re.search(r'''

\[class:(.*?)\]

''', text)
    attrs = ''
    if id_match:
        attrs += f' id="{id_match.group(1).strip()}"'
        text = text.replace(id_match.group(0), '')
    if class_match:
        attrs += f' class="{class_match.group(1).strip()}"'
        text = text.replace(class_match.group(0), '')
    return text.strip(), attrs

def parse_pagescript(pagescript):
    html_body = []
    html_head = {
        "title": "Untitled Page",
        "favicon": None,
        "scripts": []
    }

    # Default charset value; can be overridden by a [Charset:] directive.
    default_charset = "UTF-8"
    
    lines = pagescript.strip().split('\n')
    inside_table = False
    table_rows = []
    inside_script = False
    script_lines = []
    inside_div = False

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # --- Comment support ---
        if line.startswith('[Comment:') and line.endswith(']'):
            comment = line[9:-1].strip()
            html_body.append(f'<!-- {comment} -->')
            continue

        # --- Charset override ---
        if line.startswith('[Charset:'):
            match = re.match(r'''

\[Charset:\s*(.*?)\]

''', line)
            if match:
                default_charset = match.group(1).strip()
            continue

        # --- Title ---
        elif line.startswith('[Title:'):
            match = re.match(r'''

\[Title:\s*(.*?)\]

''', line)
            if match:
                html_head['title'] = match.group(1).strip()
            continue

        # --- Favicon ---
        elif line.startswith('[Favicon:'):
            match = re.match(r'''

\[Favicon:\s*(.*?)\]

''', line)
            if match:
                html_head['favicon'] = match.group(1).strip()
            continue

        # --- Image ---
        elif line.startswith('[Image:'):
            match = re.match(r'''

\[Image:\s*(.*?)\]

''', line)
            if match:
                html_body.append(f'<img src="{match.group(1).strip()}" alt="Image">')
            continue

        # --- Button ---
        elif line.startswith('[Button:'):
            match = re.match(r'''

\[Button:\s*(.*?)\s*>\s*(.*?)\]

''', line)
            if match:
                text, url = match.groups()
                html_body.append(f'<a href="{url.strip()}"><button>{text.strip()}</button></a>')
            continue

        # --- Link ---
        elif line.startswith('[Link:'):
            match = re.match(r'''

\[Link:\s*(.*?)\s*>\s*(.*?)\]

''', line)
            if match:
                text, url = match.groups()
                html_body.append(f'<a href="{url.strip()}">{text.strip()}</a>')
            continue

        # --- Unordered List ---
        elif line.startswith('[List:'):
            match = re.match(r'''

\[List:\s*(.*?)\]

''', line)
            if match:
                items = [f"<li>{item.strip()}</li>" for item in match.group(1).split('|')]
                html_body.append("<ul>\n" + "\n".join(items) + "\n</ul>")
            continue

        # --- Ordered List ---
        elif line.startswith('[OList:'):
            match = re.match(r'''

\[OList:\s*(.*?)\]

''', line)
            if match:
                items = [f"<li>{item.strip()}</li>" for item in match.group(1).split('|')]
                html_body.append("<ol>\n" + "\n".join(items) + "\n</ol>")
            continue

        # --- Table block ---
        elif line.startswith('[Table:'):
            inside_table = True
            table_rows = []
            continue

        # --- End of a block: Table, Script, or Div ---
        elif line == ']':
            if inside_table:
                if table_rows:
                    html_body.append('<table>')
                    header = table_rows[0].split('|')
                    html_body.append('<tr>' + ''.join(f'<th>{h.strip()}</th>' for h in header) + '</tr>')
                    for row in table_rows[1:]:
                        cells = row.split('|')
                        html_body.append('<tr>' + ''.join(f'<td>{c.strip()}</td>' for c in cells) + '</tr>')
                    html_body.append('</table>')
                inside_table = False
                continue
            elif inside_script:
                html_head['scripts'].append('\n'.join(script_lines))
                inside_script = False
                script_lines = []
                continue
            elif inside_div:
                html_body.append('</div>')
                inside_div = False
                continue

        # --- Inside Table block ---
        elif inside_table:
            table_rows.append(line)
            continue

        # --- Script block ---
        elif line.startswith('[Script:'):
            inside_script = True
            script_lines = []
            continue

        # --- Div Container ---
        elif line.startswith('[Div:'):
            # Process Div directive. Extract any [id:] or [class:] from the rest of the line.
            div_content = line[5:].strip()
            content, attrs = extract_attributes(div_content)
            html_body.append(f'<div{attrs}>')
            inside_div = True
            continue

        # --- Headings with ID/Class attributes ---
        elif line.startswith('#'):
            # Use extract_attributes to check for inline [id:] or [class:] directives
            content, attrs = extract_attributes(line[1:].strip())
            html_body.append(f"<h1{attrs}>{content}</h1>")
            continue

        # --- Horizontal rule ---
        elif line == '---':
            html_body.append("<hr>")
            continue

        # --- Default: Inline formatting for paragraphs ---
        else:
            if inside_script:
                script_lines.append(line)
                continue
            # Convert **bold** and *italic* syntaxes
            line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
            line = re.sub(r'\*(.*?)\*', r'<em>\1</em>', line)
            html_body.append(f"<p>{line}</p>")

    # --- Build final HTML ---
    head_lines = [f"<title>{html_head['title']}</title>"]
    if html_head['favicon']:
        head_lines.append(f'<link rel="icon" href="{html_head["favicon"]}">')
    for script in html_head['scripts']:
        head_lines.append(f"<script>\n{script}\n</script>")

    final_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="{default_charset}">
{chr(10).join(head_lines)}
</head>
<body>
{chr(10).join(html_body)}
</body>
</html>
"""
    return final_html

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python converter.py your_file.pagescript")
        sys.exit(1)

    input_path = sys.argv[1]

    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            content = file.read()
        output = parse_pagescript(content)
        output_filename = input_path.rsplit('.', 1)[0] + '.html'
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write(output)
        print(f"Successfully converted '{input_path}' → '{output_filename}'! Check your folder :)")
    except FileNotFoundError:
        print(f"File '{input_path}' not found - check the directory.")
