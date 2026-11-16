import argparse
import functools
import http.server
import os
import tempfile
import threading

from playwright.sync_api import sync_playwright

from frame import frame


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args, **kwargs):
        pass


def serve(directory):
    handler = functools.partial(Quiet, directory=directory)
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("out")
    ap.add_argument("--wait", type=int, default=2500)
    ap.add_argument("--click", default="")
    ap.add_argument("--hash", default="")
    ap.add_argument("--radius", type=int, default=28)
    args = ap.parse_args()

    server = None
    if os.path.exists(args.target):
        path = os.path.abspath(args.target)
        server = serve(os.path.dirname(path))
        url = "http://127.0.0.1:%d/%s" % (server.server_address[1], os.path.basename(path))
    else:
        url = args.target
    if args.hash:
        url += "#" + args.hash.lstrip("#")

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    tmp = tempfile.mkdtemp()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for scheme in ("light", "dark"):
            ctx = browser.new_context(viewport={"width": 1280, "height": 800}, color_scheme=scheme, device_scale_factor=2)
            page = ctx.new_page()
            page.route(
                "**/*",
                lambda r: r.abort()
                if r.request.url.startswith("http") and "127.0.0.1" not in r.request.url
                else r.continue_(),
            )
            page.goto(url)
            page.wait_for_timeout(args.wait)
            if args.click:
                page.get_by_role("button", name=args.click).first.click()
                page.wait_for_timeout(1200)
            raw = os.path.join(tmp, "raw-%s.png" % scheme)
            page.screenshot(path=raw)
            frame(raw, "%s-%s.png" % (args.out, scheme), scheme, args.radius)
            ctx.close()
        browser.close()
    if server:
        server.shutdown()


if __name__ == "__main__":
    main()
