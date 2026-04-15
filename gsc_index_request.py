"""
Google Indexing API - URLインデックス申請スクリプト
kurashi-support-navi用
"""

import subprocess
import json
import sys

URLS = [
    "https://kurashi-support-navi.com/",
    "https://kurashi-support-navi.com/about.html",
    "https://kurashi-support-navi.com/articles/bathroom-cleaning-ryokin.html",
    "https://kurashi-support-navi.com/articles/eakon-cleaning-jibun-vs-gyosha.html",
    "https://kurashi-support-navi.com/articles/eakon-cleaning-ryokin.html",
    "https://kurashi-support-navi.com/articles/fuyohin-kaishu-osusume.html",
    "https://kurashi-support-navi.com/articles/fuyohin-kaishu-ryokin.html",
    "https://kurashi-support-navi.com/articles/hitorigurase-kaji-daiko.html",
    "https://kurashi-support-navi.com/articles/house-cleaning-osusume.html",
    "https://kurashi-support-navi.com/articles/kaji-daiko-casy-review.html",
    "https://kurashi-support-navi.com/articles/kaji-daiko-hajimete.html",
    "https://kurashi-support-navi.com/articles/kaji-daiko-hitori-okaasan.html",
    "https://kurashi-support-navi.com/articles/kaji-daiko-osusume.html",
    "https://kurashi-support-navi.com/articles/kaji-daiko-otoko.html",
    "https://kurashi-support-navi.com/articles/kaji-daiko-ryokin.html",
    "https://kurashi-support-navi.com/articles/kaji-daiko-taskaji-review.html",
    "https://kurashi-support-navi.com/articles/kitchen-cleaning-ryokin.html",
    "https://kurashi-support-navi.com/articles/kurashinomarket-review.html",
    "https://kurashi-support-navi.com/articles/takuhai-cleaning-futon.html",
    "https://kurashi-support-navi.com/articles/takuhai-cleaning-osusume.html",
    "https://kurashi-support-navi.com/articles/takuhai-cleaning-suits.html",
    "https://kurashi-support-navi.com/articles/tomobataraki-kaji-daiko.html",
    # 2026-04-15 追加分
    "https://kurashi-support-navi.com/articles/kaji-daiko-sangoichijiku.html",
    "https://kurashi-support-navi.com/articles/kaji-daiko-spot.html",
    "https://kurashi-support-navi.com/articles/kaji-daiko-bears-review.html",
    "https://kurashi-support-navi.com/articles/toilet-cleaning-ryokin.html",
    "https://kurashi-support-navi.com/articles/house-cleaning-hikkoshi.html",
    "https://kurashi-support-navi.com/articles/osouji-honpo-review.html",
    "https://kurashi-support-navi.com/articles/takuhai-cleaning-ryokin.html",
    "https://kurashi-support-navi.com/articles/takuhai-cleaning-down.html",
    "https://kurashi-support-navi.com/articles/fuyohin-kaishu-hikkoshi.html",
    "https://kurashi-support-navi.com/articles/sodai-gomi-vs-kaishu.html",
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

def request_indexing(url, token):
    import urllib.request
    data = json.dumps({"url": url, "type": "URL_UPDATED"}).encode()
    req = urllib.request.Request(
        "https://indexing.googleapis.com/v3/urlNotifications:publish",
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
    print(f"取得完了\n")

    success = 0
    failed = 0

    total = len(URLS)
    for i, url in enumerate(URLS, 1):
        print(f"[{i:2d}/{total}] {url.split('/')[-1] or 'index'}", end=" ... ")
        status, body = request_indexing(url, token)
        if status == 200:
            print("OK")
            success += 1
        else:
            print(f"NG ({status}): {body.get('error', {}).get('message', body)}")
            failed += 1

    print(f"\n完了: 成功 {success}件 / 失敗 {failed}件")

if __name__ == "__main__":
    main()
