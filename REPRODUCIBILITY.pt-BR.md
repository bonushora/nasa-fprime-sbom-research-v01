# Limite de reconstrução e reprodutibilidade

## Estado

Duas execuções locais foram observadas no ambiente qualificado original. Nenhuma parte independente reconstruiu o experimento em ambiente separado.

`EXTERNAL_INDEPENDENT_REPRODUCTION=NOT_VERIFIED`

Esse estado é uma limitação, não uma falha das execuções locais e não um PASS.

## Procedimento de reconstrução

1. Obter o F Prime do repositório oficial e resolver o commit `a4b1b1c043d1f9b51a7faba4a47d5d0f231910c7`. Verificar as evidências de objetos/árvore Git e o manifesto SHA-256 de 3.609 entradas.
2. Manter o gitlink `googletest` sem materialização para reproduzir a entrada observada. Inicializá-lo muda a população de fontes e constitui outro experimento.
3. Obter o Syft 1.56.0 da release oficial da Anchore e verificar os checksums registrados.
4. Reconstruir `.artifacts/v0.2/source` e `.artifacts/v0.2/tools/syft`. Inspecionar os scripts antes da execução.
5. Recriar isolamento efetivo: fontes somente leitura; home, cache, build e instalação efêmeros e separados; rede externa negada; sem home, credenciais ou `/etc` do host; `PATH` fechado; UTC/locale C; limites documentados de recursos e tempo.
6. Executar `scripts/run-native-sbom.sh` somente em nova fase executável autorizada. A F6-R6 não reexecutou Syft nem CMake.
7. Preservar cada SPDX original antes da análise. Validar com o schema SPDX 2.3 incluído e verificar referências das relações.
8. Comparar recursivamente os documentos completos analisados e registrar todos os caminhos diferentes. Usar o comparador projetivo histórico apenas como análise secundária e limitada.
9. Comparar declarações e pacotes detectados com identificadores qualificados por ecossistema quando disponíveis. Não interpretar coincidência de nome/versão como resolução, compilação, vinculação ou distribuição.
10. Verificar o novo manifesto do pacote e registrar ambiente, operador, comandos, timestamps, códigos de saída e desvios.

## Observação local

Os dois SPDX fornecidos diferem em exatamente dois caminhos: `creationInfo.created` e `documentNamespace`. Normalizar somente esses valores torna iguais os documentos analisados completos. Isso evidencia repetibilidade nas condições locais registradas, não uma conclusão geral entre hosts, versões, estados de fonte ou datas.

## Ainda não verificado

- reconstrução externa por operador independente;
- reprodução de build e testes de um deployment completo;
- comportamento com submódulos inicializados;
- cobertura binária, de vinculação, runtime, sistema-alvo e distribuição;
- vulnerabilidades e completude de dependências.

Os SPDX originais são evidências imutáveis e não devem ser editados para remover caminhos, timestamps, UUIDs ou metadados.

