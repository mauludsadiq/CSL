# trustpass/utils/diff.py

from difflib import HtmlDiff

def generate_diff(raw_text: str, corrected_text: str, fromdesc="Raw", todesc="Corrected") -> str:
    differ = HtmlDiff(wrapcolumn=80)
    html_diff = differ.make_file(
        raw_text.splitlines(),
        corrected_text.splitlines(),
        fromdesc=fromdesc,
        todesc=todesc,
        context=True,
        numlines=3
    )
    return html_diff
