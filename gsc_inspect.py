"""
Google Search Console URL Inspection API - インデックス状況チェック
kurashi-support-navi用
"""

import subprocess
import json
import sys
import urllib.request
import time

SITE_URL = "https://kurashi-support-navi.com/"

URLS = [
    "https://kurashi-support-navi.com/",
    "https://kurashi-support-navi.com/about.html",
    "https://kurashi-support-navi.com/privacy.html",
    "https://kurashi-support-navi.com/articles/bathroom-cleaning-ryokin.html",
    "https://kurashi-support-navi.com/articles/eakon-cleaning-jibun-vs-gyosha.html",
    "https://kurashi-support-navi.com/articles/eakon-cleaning-ryokin.html",
    "https://kurashi-support-navi.com/articles/fuyohin-kaishu-hikkoshi.html",
    "https://kurashi-support-navi.com/articles/fuyohin-kaishu-osusume.html",
    "https://kurashi-support-navi.com/articles/fuyohin-kaishu-ryokin.html",
    "https://kurashi-support-navi.com/articles/hitorigurase-kaji-daiko.html",
    "https://kurashi-support-navi.com/articles/house-cleaning-hikkoshi.html",
    "https://kurashi-support-navi.com/articles/house-cleaning-osusume.html",
    "https://kurashi-support-navi.com/articles/kaji-daiko-bears-review.html",
    "https://kurashi-support-navi.com/articles/kaji-daiko-casy-review.html",
    "https://kurashi-support-navi.com/articles/kaji-daiko-hajimete.html",
    "https://kurashi-support-navi.com/articles/kaji-daiko-hitori-okaasan.html",
    "https://kurashi-support-navi.com/articles/kaji-daiko-osusume.html",
    "https://kurashi-support-navi.com/articles/kaji-daiko-otoko.html",
    "https://kurashi-support-navi.com/articles/kaji-daiko-ryokin.html",
    "https://kurashi-support-navi.com/articles/kaji-daiko-sangoichijiku.html",
    "https://kurashi-support-navi.com/articles/kaji-daiko-spot.html",
    "https://kurashi-support-navi.com/articles/kaji-daiko-taskaji-review.html",
    "https://kurashi-support-navi.com/articles/kitchen-cleaning-ryokin.html",
    "https://kurashi-support-navi.com/articles/kurashinomarket-review.html",
    "https://kurashi-support-navi.com/articles/osouji-honpo-review.html",
    "https://kurashi-support-navi.com/articles/sodai-gomi-vs-kaishu.html",
    "https://kurashi-support-navi.com/articles/takuhai-cleaning-down.html",
    "https://kurashi-support-navi.com/articles/takuhai-cleaning-futon.html",
    "https://kurashi-support-navi.com/articles/takuhai-cleaning-osusume.html",
    "https://kurashi-support-navi.com/articles/takuhai-cleaning-ryokin.html",
    "https://kurashi-support-navi.com/articles/takuhai-cleaning-suits.html",
    "https://kurashi-support-navi.com/articles/toilet-cleaning-ryokin.html",
    "https://kurashi-support-navi.com/articles/tomobataraki-kaji-daiko.html",
]

def get_access_token():
    result = subprocess.run(
        ["/Users/yamato_o/Downloads/google-cloud-sdk/bin/gcloud", "auth", "application-default", "print-access-token"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("エラー: アクセストークン取得失敗")
        print(result.stderr)
        sys.exit(1)
    return result.stdout.strip()

def inspect_url(url, token):
    data = json.dumps({
        "inspectionUrl": url,
        "siteUrl": SITE_URL,
    }).encode()
    req = urllib.request.Request(
        "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect",
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "x-goog-user-project": "project-51d120e2-4c4f-4acd-9d8",
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as res:
            return res.status, json.loads(res.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())

def main():
    print("アクセストークン取得中...")
    token = get_access_token()
    print("取得完了\n")

    indexed = []
    not_indexed = []
    errors = []

    total = len(URLS)
    for i, url in enumerate(URLS, 1):
        label = url.split("/")[-1] or "index"
        print(f"[{i:2d}/{total}] {label}", end=" ... ")

        status, body = inspect_url(url, token)

        if status != 200:
            msg = body.get("error", {}).get("message", str(body))
            print(f"エラー ({status}): {msg}")
            errors.append((label, msg))
        else:
            result = body.get("inspectionResult", {})
            index_status = result.get("indexStatusResult", {})
            verdict = index_status.get("verdict", "UNKNOWN")

            if verdict == "PASS":
                coverage = index_status.get("coverageState", "")
                print(f"インデックス済み ({coverage})")
                indexed.append(label)
            else:
                coverage = index_status.get("coverageState", verdict)
                print(f"未インデックス ({coverage})")
                not_indexed.append((label, coverage))

        time.sleep(0.5)

    print(f"\n{'='*50}")
    print(f"インデックス済み: {len(indexed)}件 / {total}件")
    print(f"未インデックス : {len(not_indexed)}件")
    print(f"エラー         : {len(errors)}件")

    if not_indexed:
        print(f"\n【未インデックス一覧】")
        for label, reason in not_indexed:
            print(f"  - {label} ({reason})")

    if errors:
        print(f"\n【エラー一覧】")
        for label, msg in errors:
            print(f"  - {label}: {msg}")

if __name__ == "__main__":
    main()
