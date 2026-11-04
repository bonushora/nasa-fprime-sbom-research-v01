# F0 — Mecanismo nativo CMake/Syft

## Resumo

O mecanismo observado integra Syft como um custom target CMake global e opcional. Se `find_program` localizar `syft`, o target participa de `ALL`, espera os targets registrados em `SBOM_DEPENDENCIES`, varre o diretório `FPRIME_PROJECT_ROOT`, emite SPDX JSON em stdout, grava o resultado no build tree por meio de `redirector.py` e aciona a instalação do componente. Se Syft não for localizado, o código apenas registra uma mensagem informativa e não cria o target observado.

Fonte principal inicial: [nasa/fprime `sbom.cmake` em `devel`](https://github.com/nasa/fprime/blob/devel/cmake/target/sbom.cmake). Em F0-R1B, o mesmo conteúdo foi confirmado nos bytes do pacote com Git blob OID `f298b0f19dc2c5febcb9d9f72f474e2b2561b1b3` e SHA-256 `aa720bb92c6f3a4525770b59a0c35830d35975f49b9cbb38096669c2643b9eae`. O vínculo desse blob ao path/tree do commit candidato ainda não foi comprovado localmente.

## Fluxo observado

1. `FPRIME__INTERNAL_SBOM_REDIRECTOR` aponta para `tools/redirector.py` e é colocado no cache interno CMake.
2. `sbom_add_global_target(TARGET)` procura um executável chamado `syft` no ambiente de configuração.
3. Quando encontrado, `add_custom_target("${TARGET}" ALL ...)` torna a geração parte do build padrão.
4. O comando chama `${PYTHON}`, o redirector e o caminho de saída `${CMAKE_BINARY_DIR}/${PROJECT_NAME}_sbom.json`.
5. O redirector executa `"${SYFT}" "dir:${FPRIME_PROJECT_ROOT}" -o spdx-json --exclude '*/**/.github'` sem shell e envia stdout ao arquivo.
6. `DEPENDS $<TARGET_PROPERTY:${TARGET},SBOM_DEPENDENCIES>` introduz dependências de build acumuladas no target global.
7. Uma regra `install(FILES ...)` associa o JSON ao componente `${TARGET}` e ao destino `${TOOLCHAIN_NAME}`.
8. Um comando `POST_BUILD` invoca CMake em modo script para instalar o componente por `fprime_install.cmake`, passando o componente, destino de instalação e build dir no conteúdo visível mais recente da página.

## Entradas e saídas

| Tipo | Elemento | Observação |
|---|---|---|
| entrada | `TARGET` | nome do custom target e do componente de instalação |
| entrada | `PATH` | escolhe o executável `syft`; não há versão fixada |
| entrada | `${PYTHON}` | interpretador usado para o redirector |
| entrada | `FPRIME_PROJECT_ROOT` | raiz inteira passada ao source `dir:` do Syft |
| entrada | configuração/ambiente Syft | não neutralizados pelo comando observado |
| entrada | `SBOM_DEPENDENCIES` | ordena o target depois dos targets CMake registrados |
| saída | `${CMAKE_BINARY_DIR}/${PROJECT_NAME}_sbom.json` | stdout de Syft em formato `spdx-json` |
| saída | `${FPRIME_INSTALL_DEST}` / `${TOOLCHAIN_NAME}` | cópia instalada, caminho final dependente do wrapper/variáveis |

## Hooks de deployment e módulo

`sbom_add_deployment_target(MODULE TARGET SOURCES DEPENDENCIES FULL_DEPENDENCIES)` e `sbom_add_module_target(MODULE TARGET SOURCE_FILES DEPENDENCIES)` verificam se `TARGET` existe e, nesse caso, acrescentam `MODULE` à propriedade `SBOM_DEPENDENCIES` do target indicado, via `append_list_property`.

Fatos importantes:

- Os parâmetros `SOURCES`, `SOURCE_FILES`, `DEPENDENCIES` e `FULL_DEPENDENCIES` não são usados no corpo observado desses hooks.
- O efeito demonstrado é dependência/ordenação de targets CMake, não transmissão de um grafo de componentes ao Syft.
- Os call sites fora do arquivo e o nome concreto do target global não foram recuperados com evidência congelada nesta F0. Sua enumeração permanece `UNKNOWN`.

## Cadeia CMake — reconciliação F0-R1B

Confirmado diretamente nos bytes verificados de `sbom.cmake`:

- definições de `sbom_add_global_target`, `sbom_add_deployment_target` e `sbom_add_module_target`;
- o target global `ALL`, sua dependência em `SBOM_DEPENDENCIES`, o argv do Syft e a instalação pós-build;
- hooks de módulo/deployment que acrescentam o módulo à propriedade do target, sem consumir os argumentos de dependências recebidos.

Declarado pelo manifesto, mas não confirmado por bytes presentes no pacote:

- `cmake/FPrime.cmake:121` chamaria `register_fprime_target(target/sbom)`;
- `cmake/target/target.cmake:96-97` faria include/dispatch global;
- o mesmo dispatcher chamaria os hooks de módulo na linha 121 e deployment na linha 140.

Essa cadeia continua `PARTIAL`: `FPrime.cmake` e `target.cmake` não estão no pacote, não há tree/archive completo para busca congelada e o próprio manifesto classifica a enumeração como não exaustiva. Portanto, os pontos de registro/dispatch são evidência declaratória do pacote, não observação local do upstream.

## Escopo da varredura e exclusões

O source de Syft é explicitamente um diretório: `dir:${FPRIME_PROJECT_ROOT}`. Isso aponta para a árvore do projeto, não para o build dir nem para o diretório de instalação. A única exclusão explícita observada é `*/**/.github`. O comentário upstream diz que a intenção é excluir `.github` fora da raiz; a semântica exata do glob depende da versão do Syft e não foi executada nesta fase.

Inferência: build products fora de `FPRIME_PROJECT_ROOT`, sysroots, pacotes do host e dependências apenas linkadas externamente não entram no universo de arquivos desse source. A dependência CMake faz a varredura ocorrer depois de targets registrados, mas não expande o diretório varrido.

## Release, plataforma e deployment

| Dimensão | Vínculo observado |
|---|---|
| release/tag | nenhum argumento de release, tag ou commit passado ao Syft |
| commit | nenhum OID passado ao Syft ou gravado explicitamente pelo CMake observado |
| plataforma/toolchain | `${TOOLCHAIN_NAME}` afeta o destino de instalação; não foi visto como metadado do comando Syft |
| deployment | deployments podem participar da ordenação; não há source ou arquivo separado por deployment no trecho observado |
| projeto | `${PROJECT_NAME}` compõe o nome do arquivo |

Conclusão: não foi observado vínculo verificável entre o JSON gerado e uma release imutável. Qualquer metadado que Syft derive por conta própria não substitui uma amarração explícita e atestada no mecanismo CMake.

## Papel de `redirector.py`

Fonte: [nasa/fprime `redirector.py` em `devel`](https://github.com/nasa/fprime/blob/devel/cmake/target/tools/redirector.py).

O helper valida apenas que recebeu ao menos um argumento após o nome do programa, abre o primeiro argumento em modo `w`, executa o restante com `subprocess.run(..., stdout=file_handle)` e devolve o return code do subprocesso. Não usa shell, não valida o JSON, não captura stderr, não torna a gravação atômica e trunca um arquivo preexistente antes de saber se Syft terá sucesso.

## Limitações desta caracterização

- Commit e hashes upstream não verificados.
- Call sites das três funções não enumerados de forma completa.
- Versão mínima/máxima de Syft e versão SPDX efetiva não fixadas no comando.
- Nenhuma execução confirmou glob, conteúdo, falhas ou caminho final instalado.
