from pygit2 import clone_repository


def clone(url: str, destination: str):
    m_clone = clone_repository(url, destination)
    m_clone.free()
