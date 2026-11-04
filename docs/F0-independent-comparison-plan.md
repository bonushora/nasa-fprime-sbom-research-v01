# F0 — Plano de comparação independente

## Estado

`PLAN_ONLY — NOT_AUTHORIZED_FOR_EXECUTION`

O objetivo futuro é comparar o mecanismo nativo a uma enumeração independente sem tratar concordância como prova automática de completude.

## Pré-condições obrigatórias

1. Autorização explícita para uma nova fase executável.
2. Commit completo do F´ congelado e arquivos obtidos por URLs imutáveis.
3. Hashes verificados do source, submódulos, ferramentas e configurações.
4. Syft, Python e CMake pinados, ambiente sem rede e workspace descartável.
5. Deployment, plataforma/toolchain e configuração de build definidos antes da coleta.
6. Critérios de aceitação aprovados sem alterar o upstream.

## Conjuntos a comparar

| Conjunto | Produção futura | Finalidade |
|---|---|---|
| NATIVE-SOURCE | target nativo F´ no ambiente isolado | observar resultado efetivo do mecanismo |
| DIRECT-SOURCE | mesma versão Syft e argv equivalente, invocação controlada | separar efeitos do wrapper/CMake |
| MANIFEST-LEDGER | parsing somente leitura dos manifests/locks no commit | inventário independente de declarações |
| BUILD-GRAPH | CMake File API/metadata gerada em build autorizado | targets e dependências do build |
| ARTIFACT-SCAN | Syft sobre install tree/artefato final, se aprovado | medir diferença source versus produto |
| LINKAGE | link maps e dependências dinâmicas do artefato, se aplicável | bibliotecas realmente ligadas |
| OFFICIAL | eventual artefato publicado pela NASA e autenticado | comparar apenas se sua existência/proveniência for verificada |

## Normalização

- Preservar os originais e trabalhar sobre cópias normalizadas.
- Registrar schema/versão; não converter silenciosamente entre formatos.
- Normalizar identificadores por PURL/CPE/ecossistema, nome, versão e origem, preservando colisões.
- Separar timestamps/IDs aleatórios de diferenças semânticas.
- Não equiparar dependência declarada, resolvida, construída, ligada e distribuída.
- Classificar cada diferença como explicação confirmada, hipótese ou desconhecida.

## Comparações e métricas

1. Reprodutibilidade byte a byte e semântica em duas execuções idênticas.
2. Componentes somente em cada conjunto e interseções por classe.
3. Versões, hashes, licenças, supplier, PURL/CPE e relações ausentes.
4. Cobertura por deployment, plataforma, build configuration e artefato.
5. Presença de commit/release e evidãncia criptográfica da associação.
6. Efeito da exclusão `.github` e de submódulos inicializados/não inicializados.
7. Diferença entre pacote detectado e arquivo meramente presente.

## Critérios de parada

Parar e registrar `BLOCKED` se identidade, hashes, isolamento de rede, pin de ferramentas ou proveniência dos resultados não puderem ser demonstrados. Falha ou divergência não autoriza ajuste ad hoc do source nem instalação de ferramentas fora do procedimento aprovado.

## Saídas futuras esperadas

Manifest de inputs, log de ambiente sanitizado, comandos, hashes de resultados originais, relatório de normalização, diff classificado e decisão separada para geração e qualificação. Este plano não estabelece que qualquer uma dessas saídas exista hoje.
