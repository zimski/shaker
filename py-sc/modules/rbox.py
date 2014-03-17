import sys,StringIO,contextlib
import nsGlobal
@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


def py_run(ssh,script,sk):
    global console
    with stdoutIO() as s:
      exec script['code'] in nsGlobal.console
    sk(2,s.getvalue())

