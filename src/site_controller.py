
from flask import Blueprint, request, render_template, Response, make_response, send_file
import markdown
import os
from pygments.formatters import HtmlFormatter
from utils import to_snake_case

site_pages = Blueprint("site_pages", __name__)

def markdown_page(path):
    if path.endswith(".md"):
        path = path[:-3]
    split_path = path.split("/")
    sanit_path = ""
    for ele in split_path:
        sanit_path = sanit_path + "/" + to_snake_case(ele)

    raw_markdown = None

    content_path = "content" + sanit_path
    content_path = content_path.replace("_", "-")

    print("Accessing " + content_path)

    if os.path.isfile(content_path + ".md"):
        with open(content_path + ".md") as f:
            raw_markdown = f.read()
    elif os.path.isfile(content_path + "/index.md"):
        with open(content_path + "/index.md") as f:
            raw_markdown = f.read()

    if raw_markdown is None:
        return render_template("404.jinja.html")

    md_template_string = markdown.markdown(
        raw_markdown, extensions=[
            "markdown.extensions.extra",
            "markdown.extensions.codehilite",
            "markdown.extensions.sane_lists"
        ]
    )
    md_template_string = md_template_string.replace("<table>", "<table class=\"table table-hover\">")
    formatter = HtmlFormatter(style="emacs",full=True,cssclass="codehilite")
    css_string = formatter.get_style_defs()
    md_css_string = "<style>" + css_string + "</style>"
    md_template_string = md_template_string.replace("<div class=\"codehilite\">", "<div class=\"codehilite container p-2 my-3 border rounded\">")
    md_template_string = md_template_string.replace("<pre>", "<pre style=\"margin:0;\">")
    md_template = md_template_string + "\n" + md_css_string

    return render_template("content_page.jinja.html", markdown=md_template)

#@site_pages.route("/content", defaults={'path': 'index'}, methods=['GET'])
#@site_pages.route("/content/", defaults={'path': 'index'}, methods=['GET'])
@site_pages.route("/<path:path>", methods=['GET'])
def main_content_route(path):
    return markdown_page(path)

