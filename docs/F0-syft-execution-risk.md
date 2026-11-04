# F0 — Risco de execução Syft

## Classificação desta fase

`EXECUTION=NOT_AUTHORIZED_AND_NOT_EXECUTED`

Esta é uma análise de superfície de efeitos, não uma constatação de vulnerabilidade.

## Ferramentas e efeitos observados

| Componente | Ação | Efeito potencial |
|---|---|---|
| CMake | resolve `syft` por `PATH` | comportamento depende do host e do binário encontrado |
| Python | executa `redirector.py` | abre/trunca o JSON de saída |
| `redirector.py` | chama argv com `subprocess.run` | executa Syft sem shell; propaga o return code; stderr permanece externo |
| Syft | cataloga `dir:${FPRIME_PROJECT_ROOT}` | leitura recursiva do projeto e interpretação de manifests/artefatos |
| CMake install | instala o componente após o target | escrita/cópia no destino de instalação configurado |

## Dependências e variabilidade do host

- Executáveis CMake, Python e Syft, todos com versão e hash não fixados no trecho observado.
- `PATH`, variáveis CMake, permissões, locale, timezone, filesystem e links simbólicos.
- Configuração, variáveis de ambiente, cache e diretórios locais que Syft possa descobrir.
- Conteúdo e estado de inicialização de submódulos na raiz varrida.
- Conjunto de catalogadores e versão do formato associados à versão de Syft encontrada.

A referência oficial atual do Syft documenta configurações para verificação de atualização, consultas remotas opcionais de ecossistemas e cache local; o comando F´ observado não fixa esses controles. Consulte [Syft Configuration Reference](https://oss.anchore.com/docs/reference/syft/configuration/) e [Supported Sources](https://github.com/anchore/syft/wiki/supported-sources).

## Efeitos colaterais possíveis

1. Criação ou truncamento do JSON no build tree, inclusive em falha de Syft.
2. Escrita da cópia instalada sob o destino configurado pelo F´.
3. Leitura ampla de todos os caminhos alcançados sob a raiz, exceto exclusões efetivas.
4. Leitura de configuração e caches do usuário; possível escrita de cache, conforme versão/configuração.
5. Tráfego de rede para update check ou enriquecimento remoto quando habilitado pela versão/configuração.
6. Uso de CPU, memória e I/O proporcional ao conteúdo varrido.
7. Mudança silenciosa de comportamento quando `syft` aparece ou desaparece do `PATH`, porque o target é condicional e integra `ALL`.

Os itens 4 e 5 são possibilidades dependentes de versão/configuração, não efeitos observados em execução nesta pesquisa.

## Limites de cobertura e confiança

- A origem é uma árvore de diretório, não a instalação final nem uma imagem executável.
- Syft identifica pacotes por catalogadores e evidências reconhecidas; isso não equivale a enumerar todo arquivo fonte ou todo target CMake.
- O grafo de link do compilador e os parâmetros `DEPENDENCIES`/`FULL_DEPENDENCIES` não são entregues ao comando Syft observado.
- Dependências ausentes da árvore, código gerado fora dela e componentes do host/toolchain podem ficar fora.
- `spdx-json` sem versão explícita pode mudar de schema/default entre versões de Syft. A documentação oficial confirma que formatos padrão podem omitir ou transformar dados presentes no formato nativo: [Output Formats](https://oss.anchore.com/docs/guides/sbom/formats/).

## Condições mínimas para futura execução isolada

Somente após nova autorização:

- congelar o commit upstream e verificar hashes de todos os inputs;
- fixar versão e SHA-256 do binário Syft, Python e CMake usados;
- usar source read-only e build/install/cache efêmeros em diretório dedicado;
- negar rede por mecanismo externo e desabilitar explicitamente update/enriquecimento remoto;
- fornecer HOME/config/cache controlados e ambiente mínimo, sem credenciais;
- usar `PATH` fechado e registrar argv e versões sem executar wrappers não revisados;
- limitar CPU, memória, I/O, tempo e espaço em disco;
- registrar árvore de inputs, estado de submódulos, toolchain, plataforma e deployment;
- validar JSON/schema e usar publicação atômica somente após return code zero;
- comparar hashes e resultados em pelo menos duas execuções idênticas antes de alegar reprodutibilidade.

## Build-generated versus oficial publicado

Um SBOM gerado pelo build é um resultado local do source tree, ferramentas e configuração daquele host. Um eventual SBOM oficial publicado precisaria ser associado pelo publicador a uma release, ter proveniência, canal, checksums/assinaturas e política de geração verificáveis. Esta F0 não estabeleceu que a NASA publique tal artefato e não trata um resultado local como oficial.
