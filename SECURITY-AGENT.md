# Agent's HY Memory dependency patch

This branch retains HY Memory functionality and is based on the published
`hy-memory-v2.0.5` source. Its downstream version is `2.0.5+agent.1`.

Both the core and `all` extra require the exact reviewed ChromaDB security
commit `00c54a0164bc0d433d92bf956bebf2a0883d77dd` from
`adybag14-cyber/chroma`. The ordinary PyPI `chromadb==1.5.9` package is not a
substitute: it is still affected by CVE-2026-45829, CVE-2026-45830,
CVE-2026-45831, and CVE-2026-45833. See that fork's `SECURITY-AGENT.md` and
collection-boundary regression suite for the source repair.

HY Memory supplies embeddings itself, so its primary and entity Chroma
collections explicitly disable Chroma's automatic embedding function. The
stored memory format and data directories are preserved.
