# NASA F´ SBOM Research v0.1 — F0

Baseline documental independente e não qualificada sobre o mecanismo nativo de geração de SBOM do NASA F´ (F Prime).

## Resultado desta fase

| Gate | Estado |
|---|---|
| `F0_DOCUMENTATION_GREEN` | `BLOCKED` |
| `SBOM_GENERATION_GREEN` | `NÃO_EXECUTADO` |
| `SECURITY_QUALIFICATION_GREEN` | `NÃO_EXECUTADO` |

O bloqueio de F0 é estrito: em 2026-11-03 a leitura remota permitiu observar arquivos oficiais na branch móvel `devel`, mas não permitiu resolver e verificar o commit completo que ela apontava. O acesso Git local falhou por resolução DNS e a API oficial não ficou disponível pelo canal de leitura. Portanto, não existe baseline upstream congelada, e nenhum valor foi presumido.

### Revisão F0-R1 — recuperação de identidade

Uma consulta externa independente forneceu o commit candidato `a4b1b1c043d1f9b51a7faba4a47d5d0f231910c7` e três Git blob OIDs. A tentativa local de revalidação em `2026-11-03T23:53:10-03:00` voltou a falhar por DNS no shell; commit, API, tree, raw e páginas imutáveis também não ficaram disponíveis pelo canal de leitura. Os identificadores foram preservados como evidência externa não revalidada, sem alterar o gate `BLOCKED`. Os SHA-256 documentais anteriores foram preservados no snapshot BH-SDP.

### Revisão F0-R1B — evidence bridge

O pacote local `.artifacts/f0-r1b-evidence/FPRIME-SBOM-F0-R1B-EVIDENCE-v01/` foi inspecionado sem executar seu verificador ou qualquer arquivo upstream. Os três arquivos transportados passaram em tamanho, SHA-256 e Git blob OID, inclusive por cálculo independente da fórmula Git blob. Isso fecha a integridade interna dos bytes do pacote, mas não fecha a identidade upstream: o pacote declara que não contém prova autocontida da tree, e não inclui `cmake/FPrime.cmake` nem `cmake/target/target.cmake` para confirmar localmente os pontos de registro/dispatch. O gate permanece `BLOCKED`.

Ainda assim, a fase produziu uma caracterização estática útil e rastreável. O código observado cria condicionalmente um target CMake `ALL`, chama Syft sobre `FPRIME_PROJECT_ROOT`, solicita `spdx-json`, exclui caminhos `.github` aninhados segundo o argumento observado, redireciona stdout para um arquivo no build tree e instala esse arquivo sob o diretório da toolchain. Isso não demonstra completude, autenticidade de release ou qualificação de segurança.

## Artefatos

- [Escopo e fronteiras](docs/F0-scope-and-boundaries.md)
- [Identidade upstream](docs/F0-upstream-identity.md)
- [Mecanismo nativo](docs/F0-native-sbom-mechanism.md)
- [Risco de execução Syft](docs/F0-syft-execution-risk.md)
- [Matriz de cobertura](docs/F0-dependency-coverage-matrix.md)
- [Plano de comparação independente](docs/F0-independent-comparison-plan.md)
- [Matriz de aceitação](docs/F0-acceptance-matrix.md)
- [Snapshot BH-SDP v2.3](governance/F0-sdp-snapshot.json)

## Convenções de evidência

- **Fato observado:** suportado diretamente por conteúdo lido ou por resultado local registrado.
- **Inferência:** consequência técnica do código observado, explicitamente marcada.
- **Hipótese:** proposição a testar em fase futura.
- **Desconhecido/limitação:** informação não demonstrada nesta fase.

Nenhum build, script upstream, teste, Syft ou instalador foi executado. Nenhum repositório upstream ou pesquisa cFS foi modificado.
