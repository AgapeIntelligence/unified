def log_result(data, filename: str = "result.txt"):
    with open(filename, "w") as f:
        f.write(str(data))

def log_progress(msg: str):
    print(f"[AO] {msg}")
