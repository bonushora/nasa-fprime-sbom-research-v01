# F0 — Identidade upstream

## Resultado

`BASELINE_FREEZE=BLOCKED`

A identidade completa de `devel` não foi verificável no momento da observação. Consequentemente, o requisito de identidade upstream da F0 falhou de forma fechada.

Na revisão F0-R1, uma referência independente forneceu um commit e três blobs candidatos, mas os endpoints oficiais imutáveis continuaram inacessíveis. Esses valores não foram promovidos a identidade verificada.

Na revisão F0-R1B, os bytes desses três arquivos foram recebidos em pacote local e seus hashes foram confirmados. A identidade de conteúdo está confirmada dentro do pacote; o vínculo upstream commit→tree→path→blob continua sem prova local autocontida.

## Registro da observação

| Campo | Valor | Classificação |
|---|---|---|
| Repositório | `https://github.com/nasa/fprime` | fato observado |
| Branch solicitada | `devel` | fato observado; referência móvel |
| Commit completo de `devel` | `UNKNOWN` | bloqueio |
| Observação local | `2026-11-03T23:43:03-03:00` | fato local |
| Observação UTC | `2026-11-04T02:43:03Z` | fato local |
| URL principal | `https://github.com/nasa/fprime/blob/devel/cmake/target/sbom.cmake` | fato observado |
| URL do helper | `https://github.com/nasa/fprime/blob/devel/cmake/target/tools/redirector.py` | fato observado |
| Blob SHA fornecido no mandato | `f298b0f19dc2c5febcb9d9f72f474e2b2561b1b3` | anteriormente observado; não revalidado |

## F0-R1 — referência externa candidata

| Campo | Valor fornecido | Estado local |
|---|---|---|
| Commit candidato | `a4b1b1c043d1f9b51a7faba4a47d5d0f231910c7` | `EXTERNAL_UNVERIFIED` |
| Blob `cmake/target/sbom.cmake` | `f298b0f19dc2c5febcb9d9f72f474e2b2561b1b3` | `EXTERNAL_UNVERIFIED` |
| Blob `cmake/target/tools/redirector.py` | `e92f70416a0ec6fe0da933a1cf698af66a8e3808` | `EXTERNAL_UNVERIFIED` |
| Blob `cmake/target/install.cmake` | `a0e14e139927c0ea125cd67134b79a460959d71b` | `EXTERNAL_UNVERIFIED` |
| Tentativa local | `2026-11-03T23:53:10-03:00` | fato local |
| Tentativa UTC | `2026-11-04T02:53:10Z` | fato local |

Vínculos commit→tree→path→blob: `NOT_VERIFIED`. Bytes imutáveis: `NOT_OBTAINED`. SHA-256 upstream local: `NOT_COMPUTED`. Call sites no commit candidato: `NOT_ENUMERATED`. Comparação com a caracterização F0: `NOT_PERFORMED`, pois o conteúdo da revisão candidata não foi recuperado.

## F0-R1B — verificação offline do pacote

Pacote: `.artifacts/f0-r1b-evidence/FPRIME-SBOM-F0-R1B-EVIDENCE-v01/`

| Item | Tamanho | SHA-256 local | Git blob OID local | Resultado |
|---|---:|---|---|---|
| `cmake/target/sbom.cmake` | 2363 | `aa720bb92c6f3a4525770b59a0c35830d35975f49b9cbb38096669c2643b9eae` | `f298b0f19dc2c5febcb9d9f72f474e2b2561b1b3` | `PASS` |
| `cmake/target/tools/redirector.py` | 236 | `a8ae0dd04044739643fd9f5f96e45dfe1f0a23e7a5fc3bf31f33b74bda5353a4` | `e92f70416a0ec6fe0da933a1cf698af66a8e3808` | `PASS` |
| `cmake/target/install.cmake` | 3246 | `279c06cf3682ee0374dc89b496c014a4af816baac8993cec04cce6066c31df43` | `a0e14e139927c0ea125cd67134b79a460959d71b` | `PASS` |

Os OIDs foram calculados com `git hash-object --no-filters` e, independentemente, como SHA-1 de `blob <size>\0<bytes>`. O `verify_evidence.py` não foi executado. Hashes do envelope: manifesto `03247b5ee641ad3bd703c0a7de40008b48b6232197d35fd4f9b03a952e3572b7`, README `54cf5e5a7b16b08ffdb19eee9780a6ddd30d344e62e952c02ecbb8542eef9ef5` e verificador não executado `0c31a42bc1ec8901b12119a0c620cbd1d8a48fca5beb7af828a1d5f917813755`.

O manifesto declara o commit `a4b1b1c043d1f9b51a7faba4a47d5d0f231910c7`, commit tree `af4e2084aa84d51e82949c42f116d91301f65d81` e trees descendentes, mas também declara que não contém prova completa dos objetos tree e que esses registros foram conferidos separadamente durante a preparação. Resultado: `PACKAGE_INTEGRITY=PASS`; `UPSTREAM_TREE_BINDING=BLOCKED`.

URLs imutáveis tentadas incluíram:

- `https://github.com/nasa/fprime/commit/a4b1b1c043d1f9b51a7faba4a47d5d0f231910c7`
- `https://api.github.com/repos/nasa/fprime/git/commits/a4b1b1c043d1f9b51a7faba4a47d5d0f231910c7`
- `https://api.github.com/repos/nasa/fprime/git/trees/a4b1b1c043d1f9b51a7faba4a47d5d0f231910c7?recursive=1`
- `https://raw.githubusercontent.com/nasa/fprime/a4b1b1c043d1f9b51a7faba4a47d5d0f231910c7/cmake/target/sbom.cmake`
- páginas `blob/<commit>/<path>` para os três arquivos.

## Arquivos upstream inspecionados

| Caminho | Referência lida | Hash upstream verificado nesta F0 | Situação |
|---|---|---|---|
| `cmake/target/sbom.cmake` | pacote atribuído ao commit candidato | Git blob e SHA-256 locais confirmados | path/tree upstream não confirmado |
| `cmake/target/tools/redirector.py` | pacote atribuído ao commit candidato | Git blob e SHA-256 locais confirmados | path/tree upstream não confirmado |
| `cmake/target/install.cmake` | pacote atribuído ao commit candidato | Git blob e SHA-256 locais confirmados | path/tree upstream não confirmado |

O hash do blob informado não foi reutilizado como hash do conteúdo atual porque: (a) ele não identifica o commit do repositório; (b) não houve resposta oficial de objeto Git que vinculasse esse blob ao caminho no head observado; e (c) o canal apresentou snapshots cacheados com idades diferentes.

## Tentativas e limites

- A página oficial da branch e as páginas dos arquivos foram legíveis.
- `git ls-remote https://github.com/nasa/fprime.git refs/heads/devel` falhou com `Could not resolve host: github.com`.
- O endpoint oficial `https://api.github.com/repos/nasa/fprime/commits/devel` não ficou acessível pelo canal de leitura.
- A página de histórico disponível estava cacheada e não representava comprovadamente o head no instante local.
- Em F0-R1, `git ls-remote` repetiu a falha DNS; os endpoints imutáveis de commit, tree, raw e blob retornaram indisponibilidade ou cache miss no canal de leitura.
- Não foi feito clone, download de archive ou execução de conteúdo upstream.

## Condição de desbloqueio

Em nova leitura autorizada, confirmar em endpoint oficial que o commit candidato existe e correspondeu à branch observada; obter ou verificar criptograficamente os objetos tree até cada path; e adquirir `cmake/FPrime.cmake`, `cmake/target/target.cmake` e uma enumeração congelada dos call sites na mesma revisão. Os bytes dos três arquivos já transportados não precisam ser executados para essa verificação.
