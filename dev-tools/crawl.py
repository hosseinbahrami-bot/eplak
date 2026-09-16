#!/usr/bin/env python3
import os, re, sys, json, urllib.request

ROOT_ID = "1OAL8GWGs8yy5pI7nl-YCexKyH-IufNew"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
CACHE = "/home/user/listcache.json"
SKIP_DIRS = {".gradle", "build", ".idea", ".vscode", "captures", ".cxx", "outputs",
             "intermediates", "generated", "tmp", ".kotlin"}

def get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", "replace")

def list_folder(fid):
    if fid in CACHE_DATA:
        return CACHE_DATA[fid]
    html = get(f"https://drive.google.com/embeddedfolderview?id={fid}&hl=en#list")
    entries = []
    for m in re.finditer(r'id="entry-([^"]+)"[\s\S]*?flip-entry-title">([^<]*)</div>', html):
        fid_, name, seg = m.group(1), m.group(2).strip(), m.group(0)
        typ = "folder" if ("drive/folders/" in seg or 'aria-label="Folder"' in seg) else "file"
        entries.append((fid_, name, typ))
    CACHE_DATA[fid] = entries
    return entries

def crawl(fid, path, out, skipped, depth=0):
    if depth > 12:
        return
    try:
        entries = list_folder(fid)
    except Exception as e:
        print("LIST FAIL", path, e, file=sys.stderr)
        return
    for cid, name, typ in entries:
        p = os.path.join(path, name)
        if typ == "folder":
            if name in SKIP_DIRS:
                skipped.append(p); continue
            crawl(cid, p, out, skipped, depth + 1)
        else:
            out.append((cid, p))

def download(fid, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    for url in (f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t",
                f"https://drive.google.com/uc?export=download&id={fid}&confirm=t"):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            r = urllib.request.urlopen(req, timeout=300)
            data = r.read()
            head = data[:300].lower()
            if len(data) < 4000 and (b"<html" in head or b"<!doctype" in head):
                continue
            with open(dest, "wb") as f:
                f.write(data)
            return True, len(data)
        except Exception as e:
            err = str(e)
    return False, err if 'err' in dir() else "failed"

if __name__ == "__main__":
    CACHE_DATA = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    out, skipped = [], []
    crawl(ROOT_ID, "app", out, skipped)
    json.dump(CACHE_DATA, open(CACHE, "w"))
    print("SKIPPED DIRS:", skipped, flush=True)
    print("FILES FOUND:", len(out), flush=True)
    with open("/home/user/manifest.tsv", "w") as f:
        for cid, p in out:
            f.write(f"{cid}\t{p}\n")
    ok = skipped_n = 0
    bad = []
    for i, (cid, p) in enumerate(out):
        dest = os.path.join("/home/user/src", p)
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            skipped_n += 1
            continue
        s, info = download(cid, dest)
        if s:
            ok += 1
            print(f"[{i+1}/{len(out)}] OK  {p} ({info} B)", flush=True)
        else:
            bad.append((cid, p, info))
            print(f"[{i+1}/{len(out)}] FAIL {p} :: {info}", flush=True)
    print(f"DONE new={ok} already={skipped_n} fail={len(bad)}", flush=True)
    with open("/home/user/failed.tsv", "w") as f:
        for cid, p, info in bad:
            f.write(f"{cid}\t{p}\t{info}\n")
