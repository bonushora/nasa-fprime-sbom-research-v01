# F0 — Escopo e fronteiras

## Mandato

Esta fase materializa somente documentação local e análise estática. A governança declarada é BH-SEP v2.3 / BH-SDP v2.3, com autorização `APPROVED — DOCUMENTATION_AND_READ_ONLY`, risco `LOW` e estado inicial `NOT_QUALIFIED`.

Workspace autorizado:

`/home/usuario/Desenvolvimento/bonushora/nasa-fprime-sbom-research-v01`

## Dentro do escopo

- Leitura de fontes públicas oficiais do repositório `nasa/fprime`.
- Inspeção estática de `cmake/target/sbom.cmake`, `redirector.py` e contexto CMake diretamente relevante.
- Registro de identidade, proveniência, riscos, cobertura conhecida e lacunas.
- Criação e validação sintática dos documentos F0 neste workspace.
- Comandos locais somente de leitura, data/hora, hashes e validação documental.

## Fora do escopo e não executado

- Build, configuração CMake do upstream, geração de SBOM ou execução de Syft.
- Execução de Python, CMake, testes ou qualquer script obtido do upstream.
- Instalação ou atualização de dependências.
- Clone, checkout ou modificação do NASA F´.
- Acesso ou modificação da pesquisa NASA cFS.
- Push, PR, discussão, publicação ou repositório remoto.
- Avaliação de vulnerabilidades, exploração ou qualificação de segurança.
- Afirmação de que existe um SBOM oficial de release do F´.

## Fronteira de evidência

As páginas oficiais acessíveis foram servidas por um canal de leitura com cache. A página de `sbom.cmake` indicou 53 linhas e a de `redirector.py`, 8 linhas. A identidade da branch não foi resolvida para um commit completo. Por isso:

1. o conteúdo é evidência de um mecanismo observado na referência móvel;
2. não é evidência de uma baseline imutável;
3. hashes upstream ausentes permanecem `UNKNOWN`;
4. o SHA `f298b0f19dc2c5febcb9d9f72f474e2b2561b1b3` é registrado apenas como blob anteriormente observado e fornecido no mandato, não como commit nem como valor revalidado nesta sessão.

### Atualização F0-R1B

O evidence bridge local permitiu revalidar os bytes transportados contra os três Git blob OIDs e SHA-256 declarados. Esta verificação substitui `UNKNOWN` somente para a integridade interna dos arquivos do pacote. Ela não demonstra, por si só, que o commit/tree oficial associa aqueles blobs aos caminhos declarados: os objetos tree e uma resposta oficial autenticada não fazem parte do pacote. A classificação da proveniência upstream permanece `BLOCKED`, e a cadeia de registro CMake permanece `PARTIAL` porque dois arquivos citados pelo manifesto não foram transportados.

## Regras para fases futuras

Qualquer fase executável exige autorização nova e explícita. O plano futuro não concede permissão para executar as ações que descreve.
