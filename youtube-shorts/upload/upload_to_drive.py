#!/usr/bin/env python3
"""
Google Drive uploader for the Shorts Design package.

Three modes:
  python3 upload_to_drive.py authurl
      -> prints the Google consent URL for you to open in your browser.

  python3 upload_to_drive.py authtoken '<redirect-url-or-code>'
      -> exchange the code (from the redirect URL you paste back) for tokens,
         save them to ./drive_token.json, print account info.

  python3 upload_to_drive.py upload <folder_id> [source_dir]
      -> upload every file in source_dir (recursively) into the Drive folder.
         Default source_dir is /root/shorts-design (the whole package).

Uses Google's shared "desktop app" OAuth client for rclone (no secret needed,
public client). Tokens are stored locally in drive_token.json next to this file.
"""
import sys, os, json, time, urllib.request, urllib.parse, mimetypes

CLIENT_ID = "202264815644-rt1o1c9evjaotbpbab10m83i8cnjk077.apps.googleusercontent.com"
REDIRECT_URI = "http://127.0.0.1:53682/auth"
TOKEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "drive_token.json")
SCOPES = "https://www.googleapis.com/auth/drive"
FOLDER_ID = "1JyLvZUtOK1HjuJ3O0-2R3Er_G-M_ASxu"

AUTH_URL = (
    "https://accounts.google.com/o/oauth2/v2/auth?"
    + urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
        "access_type": "offline",
        "prompt": "consent",
        "include_granted_scopes": "true",
    })
)


def http(method, url, headers=None, data=None):
    req = urllib.request.Request(url, method=method, headers=headers or {}, data=data)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def b64url(raw: bytes) -> str:
    import base64
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def exchange_code(code: str):
    # Google requires redirect_uri == registered one even for public clients
    body = urllib.parse.urlencode({
        "code": code,
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }).encode()
    st, resp = http("POST", "https://oauth2.googleapis.com/token",
                    headers={"Content-Type": "application/x-www-form-urlencoded"}, data=body)
    if st != 200:
        print("TOKEN EXCHANGE FAILED:", st, resp.decode(errors="replace")[:500])
        sys.exit(1)
    tok = json.loads(resp)
    with open(TOKEN_FILE, "w") as f:
        json.dump(tok, f, indent=2)
    print("TOKENS SAVED ->", TOKEN_FILE)
    return tok


def refresh_token(tok):
    body = urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "refresh_token": tok["refresh_token"],
        "grant_type": "refresh_token",
    }).encode()
    st, resp = http("POST", "https://oauth2.googleapis.com/token",
                    headers={"Content-Type": "application/x-www-form-urlencoded"}, data=body)
    if st != 200:
        print("REFRESH FAILED:", st, resp.decode(errors="replace")[:500])
        sys.exit(1)
    return json.loads(resp)


def load_tok(force_refresh=False):
    with open(TOKEN_FILE) as f:
        tok = json.load(f)
    if force_refresh or time.time() >= tok.get("expires_when", 0):
        rt = refresh_token(tok)
        tok["access_token"] = rt["access_token"]
        tok["expires_in"] = rt.get("expires_in", 3599)
        tok["expires_when"] = time.time() + int(tok["expires_in"])
        with open(TOKEN_FILE, "w") as f:
            json.dump(tok, f, indent=2)
    return tok["access_token"]


def whoami(access):
    st, resp = http("GET", "https://www.googleapis.com/drive/v3/about?fields=user",
                    headers={"Authorization": "Bearer " + access})
    if st != 200:
        print("WHOAMI FAILED:", st, resp.decode(errors="replace")[:300])
        return None
    u = json.loads(resp).get("user", {})
    print("AUTHORIZED AS:", u.get("displayName"), "<" + u.get("email", "") + ">")


def upload_file(access, name, mime, data, parent):
    # multipart/related: metadata JSON + content
    boundary = b"-------claudedrive" + b64url(os.urandom(12)).encode()
    meta = json.dumps({"name": name, "parents": [parent]}).encode()
    parts = (
        b"--" + boundary + b"\r\n"
        b'Content-Type: application/json; charset=UTF-8\r\n\r\n' + meta + b"\r\n"
        b"--" + boundary + b"\r\n"
        b"Content-Type: " + mime.encode() + b"\r\n\r\n" + data + b"\r\n"
        b"--" + boundary + b"--\r\n"
    )
    url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id,name"
    st, resp = http("POST", url,
                    headers={"Authorization": "Bearer " + access,
                             "Content-Type": "multipart/related; boundary=" + boundary.decode()},
                    data=parts)
    if st in (200, 201):
        j = json.loads(resp)
        return j.get("id")
    print("  upload failed:", name, st, resp.decode(errors="replace")[:300])
    return None


def find_folder(access, folder_id):
    st, resp = http("GET",
                    "https://www.googleapis.com/drive/v3/files/%s?fields=id,name,mimeType" % folder_id,
                    headers={"Authorization": "Bearer " + access})
    if st == 200:
        j = json.loads(resp)
        print("TARGET FOLDER:", j.get("name"), "(", j.get("mimeType"), ")")
        return True
    # maybe it's a shared folder requiring listing via children
    st2, resp2 = http("GET",
                      "https://www.googleapis.com/drive/v3/files?q=%%27%s%%27+in+parents&fields=files(id,name,mimeType)&pageSize=1000",
                      headers={"Authorization": "Bearer " + access}) if False else (0, b"")
    print("  folder lookup status:", st, resp.decode(errors="replace")[:200])
    return st == 200


def upload_tree(access, src, parent, prefix=""):
    items = sorted(os.listdir(src))
    for name in items:
        p = os.path.join(src, name)
        if os.path.isdir(p):
            print("[DIR] ", prefix + name)
            # create folder in drive
            meta = json.dumps({"name": name, "parents": [parent], "mimeType": "application/vnd.google-apps.folder"}).encode()
            st, resp = http("POST", "https://www.googleapis.com/drive/v3/files?fields=id,name",
                            headers={"Authorization": "Bearer " + access,
                                     "Content-Type": "application/json; charset=UTF-8"}, data=meta)
            if st != 200:
                print("  folder create failed:", name, st, resp.decode(errors="replace")[:200])
                continue
            fid = json.loads(resp)["id"]
            upload_tree(access, p, fid, prefix + name + "/")
        else:
            mime = mimetypes.guess_type(name)[0] or "application/octet-stream"
            with open(p, "rb") as f:
                data = f.read()
            fid = upload_file(access, name, mime, data, parent)
            print("[FILE]", name, "->", "OK" if fid else "FAILED")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "authurl"
    if mode == "authurl":
        print(AUTH_URL)
        print("\nAfter you click Allow, your browser will try to open a 'localhost' page")
        print("that shows an error. That's normal. Copy the FULL URL from the address bar")
        print("(it starts with http://127.0.0.1:53682/auth?code=...) and paste it back here.")
    elif mode == "authtoken":
        raw = sys.argv[2]
        raw = raw.strip()
        # accept either the full redirect URL or just the code
        if "code=" in raw:
            code = urllib.parse.parse_qs(urllib.parse.urlparse(raw).query)["code"][0]
        else:
            code = raw
        tok = exchange_code(code)
        tok["expires_when"] = time.time() + int(tok.get("expires_in", 3599))
        with open(TOKEN_FILE, "w") as f:
            json.dump(tok, f, indent=2)
        access = load_tok()
        whoami(access)
    elif mode == "upload":
        folder = sys.argv[2] if len(sys.argv) > 2 else FOLDER_ID
        src = sys.argv[3] if len(sys.argv) > 3 else "/root/shorts-design"
        access = load_tok(force_refresh=True)
        whoami(access)
        find_folder(access, folder)
        upload_tree(access, src, folder)
        print("\nDone. Re-upload identical files with: upload_to_drive.py upload <folder_id>")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
