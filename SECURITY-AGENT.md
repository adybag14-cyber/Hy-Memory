# Agent's HY Memory dependency patch

This branch retains HY Memory functionality and is based on the published
`hy-memory-v2.0.5` source. Its downstream version is `2.0.5+agent.2`.

Both the core and `all` extra require the exact reviewed ChromaDB security
commit `8f60a3606141bf1b388e0df57faf4982580a9384` from
`adybag14-cyber/chroma`. The ordinary PyPI `chromadb==1.5.9` package is not a
substitute: it is still affected by CVE-2026-45829, CVE-2026-45830,
CVE-2026-45831, and CVE-2026-45833. See that fork's `SECURITY-AGENT.md` and
collection-boundary regression suite for the source repair.

HY Memory supplies embeddings itself, so its primary and entity Chroma
collections explicitly disable Chroma's automatic embedding function. The
stored memory format and data directories are preserved.

The second patch requires Python 3.11, matching Agent's host baseline and the
patched Pillow/filelock releases. The SDK lock is regenerated across its
supported Python versions, including all extras. Reranking requires the
patched Transformers line; Qdrant's embedding extra requires Pillow 13.
The native Chroma closure is rebuilt from the pinned source, including its
PyO3, TLS, XML, YAML and ZIP dependency repairs. All 19 focused HY Memory
store/SDK cases pass against that rebuilt Linux wheel.
