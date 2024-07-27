from pygit2 import clone_repository
from tempfile import mkdtemp


def clone(url: str) -> str:
    tmpdir = mkdtemp()

    m_clone = clone_repository(url, tmpdir)
    m_clone.free()
    
    return tmpdir
