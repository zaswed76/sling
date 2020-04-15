from jinja2 import Template

template = Template("QLabel { color:{{tcolor}} }").render(tcolor="red")
print(template)

