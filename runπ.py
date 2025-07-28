import sys
import time
import re

SIGIL_TABLE = {
    "☲": "echo",
    "🜁": "breathe",
    "⟁": "seal",
    "🜁π": "spiral"
}

def echo(value):
    print(value)

def breathe(value):
    try:
        time.sleep(float(value))
    except ValueError:
        print("[breathe] Invalid delay")

def seal(value):
    print(f"[sealed] {value}")

OPS = {
    "echo": echo,
    "breathe": breathe,
    "seal": seal
}

def parse_line(line):
    # Match one or more emoji or special chars, then function, then value
    match = re.match(r'^(\X+)\s+([a-zA-Z_]+):"(.*)"$', line.strip(), re.UNICODE)
    if not match:
        return None, None, None
    sigil, func, val = match.groups()
    return sigil.strip(), func.strip(), val.strip()

def run(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line or line.startswith("#"):
                i += 1
                continue

            sigil, func, val = parse_line(line)
            print(f"[debug] sigil={sigil} func={func} val={val}")

            # 🔁 FIX: Just match function name, not Unicode sigil
            if func == "spiral":
                try:
                    loop_count = int(val)
                except ValueError:
                    print("[spiral] Invalid loop count")
                    return

                block = []
                i += 1
                while i < len(lines):
                    next_line = lines[i].strip()
                    if next_line.startswith("⟁ seal:"):
                        break
                    block.append(next_line)
                    i += 1

                for _ in range(loop_count):
                    for bl in block:
                        sig, fn, vl = parse_line(bl)
                        if fn in OPS:
                            OPS[fn](vl)
                        else:
                            print(f"[spiral] Unknown instruction: {bl}")
                # Process final seal
                sig, fn, vl = parse_line(lines[i].strip())
                if fn in OPS:
                    OPS[fn](vl)

            else:
                if func in OPS:
                    OPS[func](val)
                else:
                    print(f"[!] Unknown instruction: {line}")
            i += 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: runπ.py <file.πl>")
        sys.exit(1)
    run(sys.argv[1])

