# Analisador de Código Fonte

Este é um analisador de código fonte escrito em Python, projetado para realizar análises léxicas e sintáticas em arquivos de código fonte. Ele é composto por vários módulos que lidam com diferentes aspectos da análise, desde a identificação de tokens até a verificação de estruturas sintáticas.

## Funcionalidades

- **Análise Léxica**: O código fonte é analisado para identificar tokens, como palavras-chave, identificadores, números, operadores, etc. A análise léxica é realizada pelo módulo `analizador_lexico`.

- **Análise Sintática**: Após a análise léxica, o código fonte é analisado para garantir que ele esteja sintaticamente correto. Esta etapa é executada pelo módulo `analizador_sintatico`.

- **Suporte a Diferentes Tipos de Blocos**: O analisador reconhece e trata diferentes tipos de blocos, como variáveis, constantes, procedimentos, funções, estruturas de controle, etc.

## Estrutura do Código

- **Módulos de Análise**: O código está dividido em vários módulos, cada um responsável por uma parte específica da análise, como `constante`, `bloco_var`, `estrutura_de_dados`, `exp`, `if_while`, `PR` e `FP`.

- **Integração dos Módulos**: Os módulos são integrados através do script principal, onde os resultados da análise léxica são passados para a análise sintática e para os módulos específicos de cada tipo de bloco.

- **Geração de Saída**: Após a análise, o analisador gera arquivos de saída que contêm os resultados da análise sintática e quaisquer erros encontrados durante o processo.

## Utilização

Para utilizar o analisador de código fonte, basta executar o script principal, que irá analisar todos os arquivos de código fonte presentes no diretório especificado. Os arquivos de saída serão gerados no mesmo diretório, com extensões indicativas do tipo de análise realizada.


## Autor

Este projeto foi desenvolvido por [Wesley].
