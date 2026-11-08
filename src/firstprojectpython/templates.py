def html_template(body):
    return f"""<html>
<head>
<title>Documento</title>
</head>
<body>
<header>
<h1>Cabecera del documento</h1>
</header>
<main>
{body}
</main>
</body>
</html>
"""

def city_template(city):
    return f"""<li>{city[1]} ({city[4]})</li>"""