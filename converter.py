# converter.py

import re
import sys

def parse_pagescript(pagescript):
    html_body = []
    html_head = {
        "title": "Untitled Page",
        "favicon": None,
        "scripts": []
    }

    lines = pagescript.strip().split('\n')
    inside_table = False
    table_rows = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith('#'):
            html_body.append(f"<h1>{line[1:].strip()}</h1>")
        elif line == '---':
            html_body.append("<hr>")

        elif line.startswith('[Title:'):
            match = re.match(r'

\[Title:\s*(.*?)\]

', line)
            if match:
                html_head['title'] = match.group(1)

        elif line.startswith('[Favicon:'):
            match = re.match(r'

\[Favicon:\s*(.*?)\]

', line)
            if match:
                html_head['favicon'] = match.group(1)

        elif line.startswith('[Image:'):
            match = re.match(r'

\[Image:\s*(.*?)\]

', line)
            if match:
                html_body.append(f'<img src="{match.group(1)}" alt="Image">')

        elif line.startswith('[Button:'):
            match = re.match(r'

\[Button:\s*(.*?)\s*>\s*(.*?)\]

', line)
            if match:
                text, url = match.groups()
                html_body.append(f'<a href="{url}"><button>{text}</button></a>')

        elif line.startswith('[Link:'):
            match = re.match(r'

\[Link:\s*(.*?)\s*>\s*(.*?)\]

', line)
            if match:
                text, url = match.groups()
                html_body.append(f'<a href="{url}">{text}</a>')

        elif line.startswith('[List:'):
            match = re.match(r'

\[List:\s*(.*?)\]

', line)
            if match:
                items = [f"<li>{item.strip()}</li>" for item in match.group(1).split('|')]
                html_body.append("<ul>\n" + "\n".join(items) + "\n</ul>")

        elif line.startswith('[OList:'):
            match = re.match(r'

\[OList:\s*(.*?)\]

', line)
            if match:
                items = [f"<li>{item.strip()}</li>" for item in match.group(1).split('|')]
                html_body.append("<ol>\n" + "\n".join(items) + "\n</ol>")

        elif line.startswith('[Table:'):
            inside_table = True
            table_rows = []

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

        elif inside_table:
            table_rows.append(line)

        elif line.startswith('[Script:'):
            inside_script = True
            script_lines = []
        elif 'inside_script' in locals() and inside_script:
            if line == ']':
                html_head['scripts'].append('\n'.join(script_lines))
                inside_script = False
                script_lines = []
            else:
                script_lines.append(line)

        else:
            # Inline styles
            line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
            line = re.sub(r'\*(.*?)\*', r'<em>\1</em>', line)
            html_body.append(f"<p>{line}</p>")

    # Build final HTML
    head = [f"<title>{html_head['title']}</title>"]
    if html_head['favicon']:
        head.append(f'<link rel="icon" href="{html_head["favicon"]}">')
    for script in html_head['scripts']:
        head.append(f"<script>\n{script}\n</script>")

    final_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
{chr(10).join(head)}
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
        print(f"Successfully converted '{input_path}' → '{output_filename}'! Chach your folder :)")
    except FileNotFoundError:
        print(f"File '{input_path}' not found - check the directory.")
