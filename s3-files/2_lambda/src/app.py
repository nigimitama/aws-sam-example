import json
import os
import pickle
import time
import numpy as np

S3_BUCKET = os.environ["S3_BUCKET_NAME"]
MOUNT_PATH = "/mnt/s3files"

# Lambda の実行環境が初期化されたとき（コールドスタート）のみ True
_is_cold_start = True

# float64 で指定サイズ相当の要素数
_100MB_ELEMENTS = 100 * 1024 * 1024 // 8
_1000MB_ELEMENTS = 1000 * 1024 * 1024 // 8

FILES = {
    "100mb": (f"{MOUNT_PATH}/data_100mb.pkl", _100MB_ELEMENTS),
    "1000mb": (f"{MOUNT_PATH}/data_1000mb.pkl", _1000MB_ELEMENTS),
}


def create_data(_, __):
    """データを生成し、S3 Files にテスト用ファイルをアップロードする Lambda 関数"""

    results = {}

    for label, (path, n_elements) in FILES.items():
        data = np.random.random(n_elements)

        start = time.perf_counter()
        with open(path, "wb") as f:
            pickle.dump(data, f)
        elapsed = time.perf_counter() - start

        results[label] = {
            "path": path,
            "size_bytes": data.nbytes,
            "write_seconds": round(elapsed, 3),
        }
        print(
            f"[create] {label}: {data.nbytes / 1024**2:.1f} MB written in {elapsed:.3f}s"
        )

    return {"statusCode": 200, "body": json.dumps(results)}


def load_data(_, __):
    """S3 Files からテスト用ファイルをロードする Lambda 関数"""
    global _is_cold_start
    cold = _is_cold_start
    _is_cold_start = False

    # マウントされたディレクトリの内容を確認
    for entry in os.scandir(MOUNT_PATH):
        size_mb = entry.stat().st_size / 1024**2
        print(f"[ls] {entry.name}  {size_mb:.1f} MB")

    # S3 Files からファイルを2回読み込む
    results = {}
    for attempt in range(1, 3):
        for label, (path, _) in FILES.items():
            start = time.perf_counter()
            with open(path, "rb") as f:
                data = pickle.load(f)
            elapsed = time.perf_counter() - start

            results[f"{label}_attempt{attempt}"] = {
                "path": path,
                "size_bytes": data.nbytes,
                "read_seconds": round(elapsed, 3),
            }
            print(
                f"[load] cold={cold} attempt={attempt} {label}: {data.nbytes / 1024**2:.1f} MB loaded in {elapsed:.3f}s"
            )

    return {"statusCode": 200, "body": json.dumps(results)}
