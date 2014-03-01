import markdown

def vender_markdown(txt):
	return markdown.markdown(txt)

app.jinja_env.globals.update(vender_markdown=vender_markdown)