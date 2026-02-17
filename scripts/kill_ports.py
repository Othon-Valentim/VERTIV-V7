import os
import sys
import subprocess
import signal


def kill_port(port):
    """Kills any process listening on the specified port (Windows only)."""
    try:
        # Find PID using netstat
        output = subprocess.check_output(
            f"netstat -ano | findstr :{port}", shell=True
        ).decode()
        lines = output.strip().split("\n")
        pids = set()
        for line in lines:
            parts = line.split()
            if len(parts) > 4 and parts[1].endswith(f":{port}"):
                pids.add(parts[-1])

        if not pids:
            print(f"No process found on port {port}")
            return

        for pid in pids:
            print(f"Killing process {pid} on port {port}")
            subprocess.run(f"taskkill /F /PID {pid}", shell=True)

    except subprocess.CalledProcessError:
        print(f"No process found on port {port} or error running netstat.")
    except Exception as e:
        print(f"Error killing port {port}: {e}")


if __name__ == "__main__":
    ports_to_kill = [8000, 8001, 8002, 3000, 3001]  # Backend, Worker, Agents, Frontend
    for p in ports_to_kill:
        kill_port(p)
