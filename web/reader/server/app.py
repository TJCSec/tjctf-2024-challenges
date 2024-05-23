from flask import Flask, request, render_template
from requests import get
from lxml import etree
from urllib.parse import urlparse

app = Flask(__name__)

app.static_folder = "static"
MAX_LOGS = 30
log, log_count = [], 0
flag = open("flag.txt", "r").read().strip()


def get_text_repr(tree, url):
    discarded_elements = ("head", "script", "style")
    fix_url_path_tags = ("href", "src")
    discarded_attrs = ("style", "id", "class", "srcset")

    def recursive_parse(element):
        if element.tag in discarded_elements:
            element.getparent().remove(element)
            return
        for attr in discarded_attrs:
            if attr in element.attrib:
                element.attrib.pop(attr)
        for attr in fix_url_path_tags:
            if attr in element.attrib and element.attrib[attr]:
                tag_url = urlparse(element.attrib[attr])
                if not tag_url.scheme:
                    element.attrib[attr] = url + "/" + element.attrib[attr].lstrip("/")
        for child in element:
            recursive_parse(child)

    recursive_parse(tree.getroot())
    return etree.tostring(tree.getroot()).decode("utf-8")


@app.route("/")
def index():
    global log, log_count
    site_to_visit = request.args.get("site") or ""
    url = urlparse(site_to_visit)
    if not site_to_visit:
        return render_template("index.html")
    else:
        parser = etree.HTMLParser()
        try:
            response = get(site_to_visit).text
            tree = etree.fromstring(response, parser).getroottree()
            content = get_text_repr(tree, url.scheme + "://" + url.netloc)
        except Exception as e:
            print(e)
            log_count += 1
            if log_count >= MAX_LOGS:
                log.pop(0)
                log_count = MAX_LOGS
            log.append(str(e))
            tree = etree.fromstring(
                "<body>failed to load page</body>", parser
            ).getroottree()
            content = get_text_repr(tree, "")

        return render_template("site_view.html", content=content)


@app.route("/monitor")
def monitor():
    if request.remote_addr in ("localhost", "127.0.0.1"):
        return render_template(
            "admin.html", message=flag, errors="".join(log) or "No recent errors"
        )
    else:
        return render_template("admin.html", message="Unauthorized access", errors="")


@app.errorhandler(404)
@app.route("/404")
def not_found(dummy=None):
    return "requested page does not exist", 404


@app.route("/static/<path:path>")
def static_file(filename):
    return app.send_static_file(filename)
