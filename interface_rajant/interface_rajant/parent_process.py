"""Start helpers that are killed when their owning ROS node exits.

Configure Linux parent-death handling in a fresh Python interpreter before exec,
avoiding preexec_fn in ROS processes which already have reader/executor threads.
"""

import ctypes
import os
import signal
import subprocess
import sys


def popen_with_parent_lifetime(command, **kwargs):
    """Start a helper in the node's process group and tie it to the node's PID."""
    return subprocess.Popen(
        [sys.executable, os.path.abspath(__file__), str(os.getpid()), *command],
        **kwargs,
    )


def main():
    expected_parent = int(sys.argv[1])
    command = sys.argv[2:]
    if not command:
        raise ValueError('A helper command is required')
    if not sys.platform.startswith('linux'):
        raise RuntimeError('Rajant helper lifetime handling requires Linux')

    # This interpreter is single-threaded. Load libc here instead of running
    # Python/ctypes code after fork in the multithreaded ROS process.
    libc = ctypes.CDLL(None, use_errno=True)
    libc.prctl.argtypes = [ctypes.c_int] + [ctypes.c_ulong] * 4
    libc.prctl.restype = ctypes.c_int
    pr_set_pdeathsig = 1
    if libc.prctl(pr_set_pdeathsig, signal.SIGKILL, 0, 0, 0) != 0:
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error))

    # The parent may have died before the wrapper armed the death signal.
    if os.getppid() != expected_parent:
        os.kill(os.getpid(), signal.SIGKILL)

    # exec preserves both the parent-death setting and the launch process group.
    os.execvp(command[0], command)


if __name__ == '__main__':
    main()
