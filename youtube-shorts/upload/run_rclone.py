#!/usr/bin/env python3
"""Minimal pty driver to run rclone config and feed it inputs, logging all output.
Usage: python3 run_rclone.py '[[answer1,delay1],[answer2,delay2],...]'
Each answer is written to the PTY followed by \r, after the cumulative delay(s)
of preceding answers + a small settle time. All pty output is dumped to stdout."""
import pty, os, select, sys, time, json

ans = json.loads(sys.argv[1]) if len(sys.argv) > 1 else []
OUT = "/tmp/rclone_pty.out" if len(sys.argv) < 3 else sys.argv[2]

pid, fd = pty.fork()
if pid == 0:
    os.execvp("rclone", ["rclone", "config"])

out_f = open(OUT, "w")
def emit(s):
    out_f.write(s); out_f.flush()

def read_until(timeout=30):
    buf = b""
    end = time.time() + timeout
    while time.time() < end:
        r, _, _ = select.select([fd], [], [], 0.3)
        if r:
            try:
                chunk = os.read(fd, 65536)
            except OSError:
                break
            if not chunk:
                break
            buf += chunk
            emit(chunk.decode("utf-8", errors="replace"))
        # stop early if we've seen a prompt-like tail and no more data coming
        if buf and not select.select([fd], [], [], 0.2)[0]:
            pass
    return buf.decode("utf-8", errors="replace")

try:
    for inp, delay in ans:
        time.sleep(delay)
        emit("\n>>> SEND: %r\n" % (inp,))
        os.write(fd, (inp + "\r").encode())
        read_until(timeout=6)
    # final read to capture the rest (e.g., auth instructions) then wait for exit
    time.sleep(2)
    try:
        read_until(timeout=12)
    except Exception:
        pass
finally:
    try:
        os.close(fd)
    except Exception:
        pass
    os.waitpid(pid, 0)
    out_f.close()
