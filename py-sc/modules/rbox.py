import contextlib
global console
@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


def py_run(script,sk):
    with stdoutIO() as s:
      exec script in console
    sk(2,s.getvalue())

