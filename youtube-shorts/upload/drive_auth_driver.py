#!/usr/bin/env python3
"""Driver that runs `rclone config` under a PTY, feeds commands from a queue file,
and logs all output so the parent can coordinate the OAuth flow with the user."""
import os, pty, select, sys, time, json

CMD_FILE = "/tmp/rc_cmd." + os.environ.get("RCDRIVER_TAG", "0")
OUT_FILE = "/tmp/rc_out." + os.environ.get("RCDRIVER_TAG", "0")
DONE_FILE = "/tmp/rc_done." + os.environ.get("RCDRIVER_TAG", "0")

# context: which rclone invocation to run
CTX_FILE = "/tmp/rc_ctx." + os.environ.get("RCDRIVER_TAG", "0")
while not os.path.exists(CTX_FILE):
    time.sleep(0.2)
ctx = json.load(open(CTX_FILE))
cmd = ctx["cmd"]

os.makedirs(OUT_FILE.rsplit("/",1)[0], exist_ok=True) if "/" in OUT_FILE else None
# reset outputs
open(OUT_FILE, "w").close()
open(DONE_FILE, "w").close()

pid, fd = pty.fork()
if pid == 0:
    # child: run rclone
    os.execvp(cmd[0], cmd)

def append_out(text):
    with open(OUT_FILE, "a") as f:
        f.write(text)
        f.flush()

def append_done(text):
    with open(DONE_FILE, "a") as f:
        f.write(text)
        f.flush()

buffer = b""
sent_queue_pos = 0
last_sent = ""
try:
    while True:
        # read pending commands
        if os.path.exists(CMD_FILE):
            try:
                data = open(CMD_FILE).read()
            except Exception:
                data = ""
            lines = data.splitlines()
            # send each line as input (with \r)
            if len(lines) > 0:
                new_line = lines[-1] if lines else ""
                if new_line != last_sent and new_line != "":
                    os.write(fd, (new_line + "\r").encode())
                    append_out(">>> INPUT: %r\n" % (new_line,))
                    last_sent = new_line
        # read from pty
        r, _, _ = select.select([fd], [], [], 0.2)
        if r:
            try:
                chunk = os.read(fd, 4096)
            except OSError:
                break
            if not chunk:
                # child exited
                append_out("\n[PROCESS EXITED]\n")
                append_done("EXITED")
                break
            buffer += chunk
            # flush complete/partial lines
            text = buffer.decode("utf-8", errors="replace")
            append_out(text)
            if b"\n" in buffer:
                buffer = b""
            if len(text) > 0:
                pass
        # check if child still alive
        try:
            wpid, status = os.waitpid(pid, os.WNOHANG)
        except ChildProcessError:
            append_out("\n[PROCESS EXITED - reaped]\n")
            append_done("EXITED")
            break
        if wpid != 0:
            append_out("\n[PROCESS EXITED - status %r]\n" % (status,))
            append_done("EXITED")
            break
        # stop condition via done file content "STOP"
        if os.path.exists(DONE_FILE):
            try:
                dc = open(DONE_FILE).read()
            except Exception:
                dc = ""
            if "STOP" in dc:
                try:
                    os.write(fd, b"\x03")  # Ctrl-C
                except Exception:
                    pass
                break
        time.sleep(0.05)
finally:
    try:
        os.close(fd)
    except Exception:
        pass
