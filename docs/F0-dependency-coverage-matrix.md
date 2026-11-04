# F0 — Matriz de cobertura de dependências

Legenda: `IN-SCOPE` descreve arquivos potencialmente alcançáveis pelo source de diretório; `OUT-OF-SCOPE` descreve itens fora da raiz; `CONDITIONAL` depende do estado da árvore/catalogadores; `UNKNOWN` carece de evidência. Alcance não significa detecção correta como pacote.

| Classe | Alcance do source observado | Cobertura como dependência | Evidência/limite |
|---|---|---|---|
| manifests dentro de `FPRIME_PROJECT_ROOT` | `IN-SCOPE` | `CONDITIONAL` | Syft recebe a raiz; catalogador e versão não fixados |
| fontes C/C++ e headers | `IN-SCOPE` | `UNKNOWN` | estar legível não implica pacote SPDX ou relação |
| CMake modules/targets | `IN-SCOPE` como arquivos | `UNKNOWN` | grafo CMake não é passado ao Syft |
| dependências declaradas em `DEPENDENCIES`/`FULL_DEPENDENCIES` | n/a | `NOT_DIRECTLY_CONVEYED` | hooks observados ignoram esses parâmetros |
| módulos/deployments construídos | `CONDITIONAL` | `UNKNOWN` | registrados como dependências de ordenação, não como packages |
| submódulos Git inicializados sob a raiz | `IN-SCOPE` | `CONDITIONAL` | somente conteúdo materializado pode ser lido |
| submódulos não inicializados | `OUT-OF-SCOPE` material | `NOT_COVERED` | ponteiro Git não materializa o conteúdo |
| dependências vendorizadas sob a raiz | `IN-SCOPE` | `CONDITIONAL` | depende de evidências reconhecidas pelos catalogadores |
| ambiente virtual Python fora da raiz | `OUT-OF-SCOPE` | `NOT_COVERED` | source é o diretório do projeto |
| pacotes Python declarados em arquivos sob a raiz | `IN-SCOPE` | `CONDITIONAL` | restrições sem pin e resolução transitiva podem limitar precisão |
| build products fora da raiz | `OUT-OF-SCOPE` | `NOT_COVERED` | source não é `CMAKE_BINARY_DIR` |
| código gerado no build tree | `OUT-OF-SCOPE` | `NOT_COVERED` | salvo se o build tree estiver, excepcionalmente, dentro da raiz |
| artefatos de instalação | `OUT-OF-SCOPE` | `NOT_COVERED` | instalação ocorre depois da geração observada |
| bibliotecas do sistema/sysroot | `OUT-OF-SCOPE` | `NOT_COVERED` | nenhum sysroot ou filesystem alvo é passado |
| compilador, linker e toolchain host | `OUT-OF-SCOPE` | `NOT_COVERED` | `${TOOLCHAIN_NAME}` só foi observado no destino de instalação |
| bibliotecas apenas linkadas externamente | `OUT-OF-SCOPE` | `UNKNOWN/LIKELY_GAP` | nenhum link map ou grafo do linker é fornecido |
| binários/archives presentes sob a raiz | `IN-SCOPE` | `CONDITIONAL` | depende de catalogadores e opções para archives/binários |
| `.github` aninhados | `EXCLUDED_INTENT` | `NOT_COVERED` | argumento `--exclude '*/**/.github'`; sem teste de glob |
| `.github` na raiz | `UNKNOWN` | `UNKNOWN` | comentário sugere preservação da raiz; sem execução |
| identidade de release/tag/commit | n/a | `NOT_BOUND` | nenhum identificador é passado pelo comando observado |
| identidade de plataforma | n/a | `NOT_BOUND` | destino de instalação não prova metadado no SBOM |
| identidade de deployment | n/a | `NOT_BOUND` | não foi observado arquivo separado nem metadado por deployment |
| licenças | `CONDITIONAL` | `UNKNOWN` | depende do pacote, arquivos e enriquecimento/configuração |
| relações transitivas | `CONDITIONAL` | `UNKNOWN` | não há garantia geral no mecanismo observado |

## Conclusão

O mecanismo é melhor descrito como catalogação Syft de uma árvore de projeto após certos targets CMake, e não como SBOM do artefato final, do filesystem alvo ou do grafo completo de build. A matriz deve ser reavaliada com um commit e uma versão Syft congelados; nenhum campo `UNKNOWN` pode ser promovido por suposição.
