# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import difflib

from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text

try:
    # http://code.google.com/p/google-diff-match-patch/
    from diff_match_patch import diff_match_patch
except ImportError:
    dmp = None
else:
    dmp = diff_match_patch()


def highlight_diff(diff_text):
    """
    Simple highlight a diff text in the way pygments do it ;)
    """
    html = ['<pre class="revision-block">']
    for line in diff_text.splitlines():
        line = escape(line)
        if line.startswith("+"):
            line = '<ins>%s</ins>' % line
        elif line.startswith("-"):
            line = '<del>%s</del>' % line
        html.append(line)
    html.append("</pre>")
    html = "\n".join(html)
    return html


SEMANTIC = 1
EFFICIENCY = 2
LINE_COUNT_4_UNIFIED_DIFF = 4


def html_diff_custom(value1, value2, cleanup=SEMANTIC):
    """
    Generates a diff used google-diff-match-patch is exist or ndiff as fallback

    The cleanup parameter can be SEMANTIC, EFFICIENCY or None to clean up the diff
    for greater human readibility.
    """
    value1 = force_text(value1)
    value2 = force_text(value2)
    if dmp is not None:
        # Generate the diff with google-diff-match-patch
        diff = dmp.diff_main(value1, value2)
        if cleanup == SEMANTIC:
            dmp.diff_cleanupSemantic(diff)
        elif cleanup == EFFICIENCY:
            dmp.diff_cleanupEfficiency(diff)
        elif cleanup is not None:
            raise ValueError("cleanup parameter should be one of SEMANTIC, EFFICIENCY or None.")
        html = dmp.diff_prettyHtml(diff)
        html = html.replace("&para;<br>", "</br>")  # IMHO mark paragraphs are needlessly
    else:
        # fallback: use built-in difflib
        value1 = value1.splitlines()
        value2 = value2.splitlines()

        if len(value1) > LINE_COUNT_4_UNIFIED_DIFF or len(value2) > LINE_COUNT_4_UNIFIED_DIFF:
            diff = unified_diff(value1, value2, n=2)
        else:
            diff = difflib.ndiff(value1, value2)

        diff_text = "\n".join(diff)
        html = highlight_diff(diff_text)

    html = mark_safe(html)
    return html
