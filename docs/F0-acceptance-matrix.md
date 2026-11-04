# F0 — Matriz de aceitação

## Decisão

`F0_DOCUMENTATION_GREEN=BLOCKED`

O workspace e a documentação foram materializados, mas o gate obrigatório de identidade upstream não foi satisfeito. O resultado não é promovido a `PASS` pela mera existência dos arquivos.

| ID | Critério | Evidência | Resultado |
|---|---|---|---|
| F0-01 | workspace documental existe | nove artefatos requeridos no workspace autorizado | `PASS` |
| F0-02 | identidade upstream verificada e registrada | bytes/hashes do pacote confirmados; commit/tree/path→blob ainda sem prova autocontida | `BLOCKED` |
| F0-03 | integração CMake/Syft caracterizada | definições e comportamento confirmados; registro/dispatch apenas declarados e enumeração não exaustiva | `PARTIAL` |
| F0-04 | risco de execução delimitado | entradas, ferramentas, efeitos, host, rede/cache e isolamento documentados | `PASS` |
| F0-05 | matriz explicita conhecido/desconhecido | matriz por classe com gaps e condições | `PASS` |
| F0-06 | plano de comparação independente | conjuntos, precondições, métricas e stop rules | `PASS` |
| F0-07 | documentos inspecionados e validados | validações locais de arquivos, JSON, links/campos e hashes documentais | `PASS` |
| F0-08 | snapshot BH-SDP v2.3 consistente | `governance/F0-sdp-snapshot.json` válido e alinhado aos gates | `PASS` |

## Gates operacionais

| Gate | Resultado | Motivo |
|---|---|---|
| upstream ref resolution | `FAIL/BLOCKED` | commit candidato externo não revalidado contra `devel` |
| evidence package integrity | `PASS` | tamanhos, SHA-256 e Git blob OIDs coincidem |
| immutable source bytes | `PASS_WITH_LIMITS` | bytes locais confirmados; proveniência tree/path não confirmada |
| static source read | `PASS_WITH_LIMITS` | arquivos principais visíveis em fonte oficial cacheada |
| upstream tree binding | `FAIL/BLOCKED` | pacote não contém prova completa dos objetos tree |
| mechanism characterization | `PARTIAL` | mecanismo interno confirmado; registro/dispatch e call sites incompletos |
| risk boundary | `PASS` | nenhuma execução necessária para delimitação |
| local artifact set | `PASS` | conjunto requerido presente |
| JSON syntax | `PASS` | validação local prevista/executada antes da entrega |
| forbidden execution | `PASS` | build/Syft/testes/scripts/instalação não executados |

## Estados independentes

- `F0_DOCUMENTATION_GREEN=BLOCKED`
- `SBOM_GENERATION_GREEN=NÃO_EXECUTADO`
- `SECURITY_QUALIFICATION_GREEN=NÃO_EXECUTADO`
- `GLOBAL_GREEN=NOT_DECLARED`

## Lacunas que impedem PASS

1. Verificação oficial/local de que o commit candidato corresponde à branch observada.
2. Verificação commit→tree→path→blob para os três OIDs fornecidos.
3. Bytes verificáveis de `cmake/FPrime.cmake` e `cmake/target/target.cmake` na mesma revisão.
4. Enumeração completa dos call sites das funções `sbom_add_*` no mesmo commit.

Essas lacunas exigem nova leitura oficial; não exigem nem autorizam build ou geração de SBOM.
