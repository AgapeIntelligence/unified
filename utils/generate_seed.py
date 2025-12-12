import ast
import hashlib
import zlib
import json
from collections import defaultdict
from PIL import Image
import numpy as np
import os
def extract_bricks(root_dir: str) -> dict:
    bricks = {}
    seen = set()
    for current_root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                path = os.path.join(current_root, file)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        code = f.read()
                    tree = ast.parse(code)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            func_code = ast.get_source_segment(code, node)
                            if func_code:
                                h = hashlib.sha256(func_code.encode()).hexdigest()
                                if h not in seen:
                                    seen.add(h)
                                    rel = os.path.relpath(path, root_dir).replace(os.sep, '_')
                                    bricks[f"{node.name}_{rel}"] = func_code.strip()
                except:
                    continue
    return bricks
def build_seed():
    unified_bricks = extract_bricks('.')
    sovariel_path = 'sovariel_core'
    sovariel_bricks = extract_bricks(sovariel_path) if os.path.exists(sovariel_path) else {}
    all_bricks = {**unified_bricks, **sovariel_bricks}

    graph = defaultdict(list)
    for name, code in all_bricks.items():
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    if node.func.id in all_bricks:
                        graph[name].append(node.func.id)
        except:
            continue

    packet = {
        'version': '2025.12.12-final',
        'brick_count': len(all_bricks),
        'bricks': all_bricks,
        'graph': dict(graph)
    }
    return zlib.compress(json.dumps(packet, separators=(',', ':')).encode())
def embed_seed_in_image(seed: bytes, output_path: str = "real_evieseed.png"):
    img = Image.new('RGB', (512, 512), color=(8, 16, 32))
    arr = np.array(img, dtype=np.uint8)
    bits = ''.join(format(b, '08b') for b in seed)
    idx = 0
    for y in range(512):
        for x in range(512):
            for c in range(3):
                if idx < len(bits):
                    arr[y, x, c] = (arr[y, x, c] & 0xFE) | int(bits[idx])
                    idx += 1
    Image.fromarray(arr).save(output_path)
    print(f"Generated {output_path} - {len(seed)} bytes compressed -> {os.path.getsize(output_path)} bytes on disk")
if __name__ == "__main__":
    seed = build_seed()
    packet = json.loads(zlib.decompress(seed).decode())
    print(f"Built seed with {packet['brick_count']} unique bricks, {len(seed)} bytes compressed")
    embed_seed_in_image(seed)
