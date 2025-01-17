# -*- encoding: utf-8 -*-

TEMPLATE_html = """
<html>
<head>
<title>Report</title>
</head>
<body>
${content}
</body>
</html>
"""

TEMPLATE_host = """
<h2>${host}</h2>
<ul>
${list}
</ul>
"""

TEMPLATE_severity_high = """
 <li class="high">[${status}] <a href="${url}" target="_blank">${url}</a></li>
"""

TEMPLATE_severity_normal = """
 <li class="normal">[${status}] <a href="${url}" target="_blank">${url}</a></li>
"""
