# Codebench Extractor

> Um extrator de dados escrito em Python para o dataset do Juíz Online Codebench da Universidade Federal do Amazonas.

> Keywords: `extrator`, `codebench`, `python`, `data-mining`

<!-- TABLE OF CONTENTS -->
## Sumário

- [Sobre o Projeto](#sobre-o-projeto)
	- [Condebench](#condebench)
	- [Dataset](#dataset)
	- [Estrutura do projeto](#estrutura-do-projeto)
- [Arquivos de Saída](#release-history)
- [Tecnologias e módulos utilizados](#tecnologias-e-módulos-utilizados)
    - [Python3](#python3)
    - [os](#os)
    - [keyword](#keyword)
    - [re](#re)
    - [datetime](#datetime)
    - [radon](#radon)
    - [tokenize](#tokenize)
    - [csv](#csv)
    - [logging](#arquivos-de-saída)
- [Contato](#contato)
- [License](#license)

## Sobre o Projeto

### Codebench

O CodeBench (http://codebench.icomp.ufam.edu.br/) é um sistema juiz online, desenvolvido pelo Instituto de Computação da Universidade Federal do Amazonas, que tem por objetivos: 

- prover ao discente de disciplinas de programação um conjunto de ferramentas pedagógicas capazes de estimular e facilitar seu aprendizado;
- prover o docente com informações úteis sobre a caminhada do aluno nas disciplinas de programação;
- dispor um conjunto de ferramentas capazes de simplificar o trabalho docente; e
- fomentar e apoiar professores no desenvolvimento e/ou implementação de práticas de ensino mais modernas e criativas.

Através do Codebench, os professores podem disponibilizar exercícios de programação para seus alunos, que por sua vez devem desenvolver soluções para tais exercícios e submetê-las através da interface do sistema. O Ambiente de Desenvolvimento Integrado, ou Integrated Development Environment (IDE), utilizado pelos alunos para desenvolver as soluções dos exercícios propostos, atualmente suporta as principais funcionalidades de um IDE típico, tais como: 

- autocompletion;
- autosave;
- syntax highlighting;
- busca e substituição de strings; e
- etc.

Uma vez que um aluno submete uma solução para um dado exercício, o sistema informa instantaneamente ao aluno se sua solução está correta ou errada. As soluções são verificadas por meio de casos de teste. Ao cadastrar um dado exercício no sistema, o professor ou monitor deverá informar um ou mais casos de testes que serão usados para julgar a corretude dos códigos submetidos pelos alunos. Um caso de teste é formado por um par <E, S>, onde E é a entrada passada ao código do aluno, e S é a saída correta para a entrada fornecida. Por exemplo, considerando um exercício em que o aluno deverá imprimir o quadrado de um valor fornecido, os casos de teste deste exercícios poderiam ser: <1, 1>, <6, 36> e <12, 144>.

Atualmente, o CodeBench suporta as seguintes linguagens de programação: C, C++, Java, Python, Haskell e Lua. Além dessas linguagens, o ambiente também suporta a linguagem SQL, para exercícios envolvendo consultas a bancos de dados. Ao criar um dado trabalho, o professor ou monitor deverá informar qual linguagem será usada pelos alunos para desenvolver as soluções dos exercícios de programação desse trabalho. Além disso, o CodeBench permite a troca de mensagens entre alunos e professores de uma dada turma, bem como o compartilhamento de recursos didáticos por parte dos professores.


### Dataset

O CodeBench registra automaticamente todas as ações realizadas pelos alunos no IDE incorporado durante suas tentativas de resolver os exercícios propostos. Atualmente o conjunto de dados contém todos os registros coletados de alunos CS1 durante os semestres letivos compreendidos entre 2016 e 2019. Os dados estão distribuídos em diversos arquivos, organizados numa estrutura hierárquica de diretórios.

Devido a organização semi-estruturada e distribuída dos dados, fez-se necessário organizá-los segundo algum critério. Para tanto, desenvolvemos em Python um extrator automatizado, capaz de percorrer todo o conjunto de dados, minerando e organizando as informações disponíveis. Mais informações sobre o dataset podem ser obtidas em: http://codebench.icomp.ufam.edu.br/dataset/

### Estrutura do projeto

O projeto está organizado segundo a estrutura abaixo:

```
codebench-extractor
└─── __init__.py
└─── extractor.py
└─── model.py
└─── parser.py
└─── util.py
│
│ LICENSE
│ README.md
```

O arquivo `__init__.py` é o ponto de entrada do projeto, e por isso deve ser executado usando o interpretador Python. Dentro dele, o diretório para o dataset deve ser informado na variável `__dataset_dir__` para que o extrator possa fazer uma varredura em toda a estrutura de pastas, identificando `períodos`, `turmas`, `atividades`, `estudantes`, `execuções` e `soluções`.

O arquivo `extractor.py` contem a declaração da classe `CodebenchExtractor`. Esta classe disponibiliza métodos estáticos que recebem caminhos para diretórios ou pastas, de onde devem ser extraídas informações.

O arquivo `model.py` contem a declaração de todas as classes de modelo de dados (entidades) utilizadas pelo extrator, e que posteriormente serão salvas em arquivos `.csv`. Essas entidades são:

- `CSVEntity`: interface que expões métodos para objetos (entidade) que serão salvas em arquivos `.csv`.
- `Periodo`: classe para objetos que representam os períodos letivos.
- `Turma`: classe para objetos que representam as turmas de estudantes num período letivo.
- `Atividade`: classe para objetos que representam as atividades realizada numa turma.
- `Estudante`: classe para objetos que representam os estudantes matrículados numa turma.
- `Execucao`: classe para objetos que sumarizam as informações coletadas durante a tentativa de um estudante solucionar uma questão.
- `Solucao`: classe para objetos que sumarizam as métricas extraídas da solução de um instrutor para uma questão.
- `Erro`: classe para objetos que contabiliza as ocorrências de um tipo de erro, que foi cometido por um estudante durante a tentativa de solucionar uma questão.

O arquivo `parser.py` contem a declaração da classe `CSVParser`. Esta classe expões métodos estáticos para salvar as informações do dataset em arquivos `.csv`. As informações ao serem extraídas são mapeadas em objetos do modelo de dados e estes sim são passados como argumentos dos métodos estáticos. Dentro da classe `CSVParser` existem algumas variáveis de configuração para definir onde os dados devem ser salvos:
- `__output_dir`: diretório dos arquivos de saída. Por padrão é criado um diretório `csv` na raiz do projeto.
- `__periodos_csv`: nome do arquivos de saída para os dados de períodos letivos extraídos do dataset.
- `__turmas_csv`: nome do arquivos de saída para os dados de turmas extraídps do dataset.
- `__atividades_csv`: nome do arquivos de saída para os dados de atividades extraídos do dataset.
- `__estudantes_csv`: nome do arquivos de saída para os dados de estudantes extraídos do dataset.
- `__execucoes_csv`: nome do arquivos de saída para os dados de execuções/submissões extraídos do dataset.
- `__solucoes_csv`: nome do arquivos de saída para os dados de soluções de instrutores extraídos do dataset.
- `__erros_csv`: nome do arquivos de saída para os dados de erros cometidos por estudantes extraídos do dataset.

O arquivo `util.py` contem a declaração de duas classes: `Util` e `Logger`. A classe `Util` disponibilizada algumas funções utilitárias que são usadas dentro do projeto, limpeza do console e congelar a saída do console aguardando por uma entrada do usuário, por exemplo. A classe `Logger` é reponsável pelo gerenciamento dos `logs` gerados pelo extrator. As informações um resumo de quais informações puderam ser extraídas e também registro de erros ocorridos durante o processo de extração são armazenados em arquivos de `log`. Os arquivos são salvos por padrão na pasta `logs`, criada na raiz do projeto. A cada execução são gerados três arquivos de `log` inciados pela data e hora de execução do extrator:

- `<data_hoje>_info.log`: registra cada entidade encontrada pelo extrator.
- `<data_hoje>_warn.log`: registra avisos de eventos não esperados durante a extração (ausência do código de solução ou arquivo corrompido, por exemplo).
- `<data_hoje>_error.log`: registra as falhas ocorridas durante a extração. Em geral essas falhas são ocorridas na etapa de extração de métricas dos códigos de solução. Alguns destes códigos podem ser incompletos, gerando problemas para as bibliotecas de extração de métricas.

## Arquivos de saída

As informações extraídas do dataset são estruturadas em arquivos `csv`.

### Períodos

Os arquivo `periodos.csv` armazena das informações extraídas de todos os períodos letivos registrados:

- `descricao`: string -  descrição do período letivo (ano e semestre).

### Turmas

Os arquivo `turmas.csv` armazena das informações extraídas de todas turmas registradas:

- `periodo`: string - descrição do período letivo (ano e semestre).
- `codigo`: int - código da turma.
- `descricao`: string - descrição da turma (disciplina + estudantes).

### Estudantes

Os arquivo `estudantes.csv` armazena das informações extraídas de todos os estudantes registrados:

-- `periodo`: string - Descrição do Período (ano e número do semestre) no qual a Turma ocorreu.
- `turma`: int - Código da Turma (Disciplina) que o Estava matriculado.
- `codigo`: int - Código numérico único que identifica o Estudante.
- `curso_id`: int - Código numérico único do Curso de Graduação que o Estudante estava matriculado.
- `curso_nome`: string - Descrição do Curso de Graduação que o Estudante estava matriculado.
- `instituicao_id`: int - Código numérico único da Instituição de Ensino Superior na qual o Estudante estava matriculado.
- `instituicao_nome`: string - Descrição da Instituição de Ensino Superior (nome) na qual o Estudante estava matriculado.
- `escola_nome`: string - Descrição da Instituição de Ensino Médio (nome) da qual o Estudante é proveniente.
- `escola_tipo`: string - Tipo da Instituição de Ensino Médio da qual o Estudante é proveniente. Pode ser:
    - `private school` (escola particular),
    - `public school` (escola pública),
    - `technical school` (escola de ensino médio integrado ao técnico).
- `escola_turno`: string - Turno no qual o Estudante estudou. Pode ser:
    - `morning shift` (manhã),
    - `full-time school` (integral),
    - `afternoon shift` (tarde),
    - `night shift` (noturno).
- `escola_ano_grad`: int - Ano de graduação do Estudante no Ensino Médio.
- `sexo`: string - Sexo do Estudante. Pode ser:
    - `male` (masculino),
    - `female` (feminino).
- `ano_nascimento`: int - Ano de nascimento do Estudante.
- `estado_civil`: string - Estado Civil do Estudante. Pode ser:
    - `single` (solteiro),
    - `married` (casado),
    - `widower` (viúvo).
- `tem_filhos`: boolean - Booleano indicando se o Estudante possui ou não filhos.

### Atividades

Os arquivo `atividades.csv` armazena das informações extraídas de todas as atividades realizadas:

- `periodo`: string - Descrição do Período (ano e semestre) no qual a atividade ocorreu.
- `turma`: int - Código da Turma na qual a Atividade foi aplicada.
- `codigo`: int - Código da Atividade.
- `titulo`: string - Título da Atividade (Descrição).
- `data_inicio`: datetime - Data e Hora do início (liberação) da Atividade. No formato `YYYY-MM-DD HH:MM:SS`.
- `data_termino`: datetime - Data e Hora do encerramento da Atividade (prazo de entrega). No formato `YYYY-MM-DD HH:MM:SS`.
- `linguagem`: string - Linguagem de Programação utilizada nos Exercícios (Questões) da Atividade.
- `tipo`: string - Tipo da Atividade. Pode ser `exam` (prova/avaliação) ou `homework` (trabalho ou lista de exercícios).
- `peso`: float - Peso da Atividade na média final do Estudante.
- `n_blocos`: int - Quantidade de Blocos de Exercícios existentes na Atividade.
- `blocos`: list - Lista com os Blocos de Exercícios. Um Bloco pode ser composto de um único Código de Exercício ou uma Lista dos Códigos de todos os Exercícios que compões o Bloco.

### Execuções

O arquivo `execucoes.csv` armazena as informações extraídas das tentativas dos estudantes de solucionar uma questão.

- `periodo`: string - Descrição do Período (ano e número do semestre).
- `turma`: string - Código da Turma (Disciplina) que o Estudante estava matriculado.
- `estudante`: int - Código numérico único que identifica o Estudante.
- `atividade`: int - Código numérico único que identifica a Atividade.
- `exercicio`: int - Código numérico único que identifica o Exercicio (questão).
- `tempo_foco`: time - Tempo em segundos em que o Estudante interagiu com o Editor do CodeMirror, dentro do intervalo de duração da Atividade, desconsiderando os intervalos de interações superiores a 5 min (inatividade).
- `tempo_total`: time - Tempo Total em segundos em que o Estudante interagiu com o Editor do CodeMirror, dentro do intervalo de duração da Atividade.
- `n_submissoes`: int - Quantidade vezes em que o Estudante submeteu sua Solução  para correção automática.
- `n_testes`: int - Quantidade vezes em que o Estudante executou sua Solução para teste.
- `n_erros`: int - Quantidade Erros acusados pelo Interpretador Python durante Submissões ou Testes da Solução.
- `t_execucao`: float - Tempo em segundos que a solução do estudante levou para executar os casos de testes.
- `nota_final`: float - Maior Nota obtida por um Estudante nas tentativas de solucionar um Exercício.
- `acertou`: boolean - Booleano indicando se o Estudante conseguiu acertar a questão.
- McCabe’s complexity (métricas de complexidade):
    - `complexity`: float - __Complexidade Ciclomática__ Total.
    - `n_classes`: int - Número de __Classes__ declaradas no código do estudante.
    - `n_functions`: int - Número de __Funções__ declaradas no código do estudante.
- Raw metrics (métricas de código):
    - `loc`: int - Número Total de __Linhas de Código__.
    - `lloc`: int - Número Total de __Linhas Lógicas de Código__.
    - `sloc`: int - Número de Linhas de __Código Fonte__.
    - `single_comments`: int - Número de __Comentários__.
    - `comments`: int - Número de Linhas de __Docstrings__.
    - `multilines`: int - Número de __Multi-line strings__.
    - `black_lines`: int - Número de __Linhas em branco__.
- Halstead metrics (métricas de software):
    - `h1`: int - Número de __Operadores Distintos__.
    - `h2`: int - Número de __Operandos Distintos__.
    - `N1`: int - Número __Total de Operadores__.
    - `N2`: int - Número __Total de Operandos__.
    - `vocabulary`: int - __Vocabulário__ (`h = h1 + h2`).
    - `length`: int - __Tamanho__ (`N = N1 + N2`).
    - `calculated_N`: float - __Tamanho Estimado/Calculado__ em Byte (`h1*log2(h1) + h2*log2(h2)`).
    - `volume`: float - __Volume__ (`V = N * log2(h)`).
    - `difficulty`: float - __Dificuldade de Entendimento__ (`D = h1/2 * N2/h2`).
    - `effort`: float - __Esforço de Implementação__ (`E = D * V`).
    - `time`: float - __Tempo de Implementação__ (`T = E / 18 segundos`).
    - `bugs`: float - __Estimativa de Bugs/Erros__ na implementação (`B = V / 3000`).
- Tokens (obtidos do código fonte):
    - `imports`: int - quantidade de __linhas de importação__
    - `assignments` int - quantidade total de __operações de atribuição__ (incluindo atribuição combinada com outros operadores)
    - `assignments_unique`: int - quantidade de __operadores de atribuição distintos__
    - `kwds`: int - quantidade total de __keywords__
    - `kwds_unique`: int - quantidade de __keywords distintas__
    - `lt_numbers`: int - quantidade de __constantes numéricas__
    - `lt_strs`: int - quantidade de __constantes de texto (strings)__
    - `lt_bools`: int - quantidade de __constantes booleanas__
    - `lgc_op`: int - quantidade total de __operadores lógicos__
    - `lgc_op_unique`: int - quantidade de __operadores lógicos distintos__
    - `and_op`: int - quantidade total do __operador lógico 'and'__
    - `or_op`: int - quantidade total do __operador lógico 'or'__
    - `not_op`: int - quantidade total do __operador lógico 'not'__
    - `arithmetic_op`: int - quantidade total de __operadores aritméticos__
    - `arithmetic_op_unique`: int - quantidade de __operadores aritméticos distintos__
    - `add_op`: int - quantidade total do __operador adição '+'__
    - `minus_op`: int - quantidade total do __operador substração '-'__
    - `mult_op`: int - quantidade total do __operador multiplicação '*'__
    - `div_op`: int - quantidade total do __operador divisão ponto-flutuante '/'__
    - `mod_op`: int - quantidade total do __operador módulo '%'__
    - `power_op`: int - quantidade total do __operador potência '**'__
    - `div_floor_op`: int - quantidade total do __operador divisão inteira '//'__
    - `cmp_op`: int - quantidade total de __operadores relacionais__
    - `cmp_op_unique`: int - quantidade de __operadores relacionais distintos__
    - `equal_op`: int - quantidade total do __operador igualdade '=='__
    - `not_eq_op`: int - quantidade total do __operador desigualdade '!='__
    - `le_op`: int - quantidade total do __operador menor ou igual que '<='__
    - `ge_equal_op`: int - quantidade total do __operador maior ou igual que '>='__
    - `lt_op`: int - quantidade total do __operador menor que '<'__
    - `gt_op`: int - quantidade total do __operador maior que '>'__
    - `bitwise_op`: int - quantidade total de __operadores bit-a-bit__
    - `bitwise_op_unique`: int - quantidade de __operadores bit-a-bit distintos__
    - `bitwise_and`: int - quantidade total do __operador bit-a-bit and '&'__
    - `bitwise_or`: int - quantidade total do __operador bit-a-bit or '|'__
    - `bitwise_xor`: int - quantidade total do __operador bit-a-bit xor '^'__
    - `bitwise_not`: int - quantidade total do __operador bit-a-bit not (comp) '~'__
    - `lshift_op`: int - quantidade total do __operador left shift '<<'__
    - `rshift_op`: int - quantidade total do __operador right shift '>>'__
    - `identity_op`: int - quantidade total do __operador is__
    - `membership_op`: int - quantidade total do __operador in__
    - `conditionals`: int - quantidade total de __estruturas condicionais__ (if, elif, else)
    - `ifs`: int - quantidade total de __if's__
    - `elifs`: int - quantidade total de __elif's__
    - `elses`: int - quantidade total de __else's__
    - `loops`: int - quantidade total de __estruturas de repetição__ (while, for)
    - `whiles`: int - quantidade total de __while's__
    - `fors`: int - quantidade total de __for's__
    - `breaks`: int -  quantidade de __break's__
    - `continues`: int -  quantidade de __continue's__
    - `builtin_f`: int - quantidade total de __built-in functions__
    - `builtin_f_unique`: int - quantidade de __built-in functions__ distintas
    - `type_f`: int - quantidade total de funções de __casting/tipo__ (list, tuple, str, int, float ...)
    - `type_f_unique`: int - quantidade de funções de __tipo distintas__
    - `lambdas`: int - quantidade de __lambda expressions__
    - `lpar`: int - quantidade total de __(__
    - `rpar`: int - quantidade total de __)__
    - `lsqb`: int - quantidade total de __[__
    - `rsqb`: int - quantidade total de __]__
    - `lbrace`: int - quantidade total de __{__
    - `rbrace`: int - quantidade total de __}__
    - `commas`: int - quantidade total de __,__
    - `colons`: int - quantidade total de __:__
    - `dots`: int - quantidade total de __.__
    - `prints`: int - quantidade total de ocorrências da função __print (saídas)__
    - `inputs`: int - quantidade total de ocorrências da função __input (entradas)__
    - `len`: int - quantidade total de ocorrências da função __len (tamanho de sequences)__
    - `uident`: int - quantidade total de __user identifiers__
    - `uident_unique`: int - quantidade de __user identifiers distintos__
    - `uident_mean`: float - proporção __user identifiers__ por __linhas de código com identifiers__
    - `uident_per_line`: float - proporção de __user identifiers__ por linhas de código (loc), (__quantidadelinhas de código com identifiers__
    - `uident_chars`: float - proporção de __caracteres nos nomes dos identificadores__

### Soluções

O arquivo `soluções.csv` armazena as informações extraídas dos códigos de solução elaborados pelos instrutores.

- `codigo`: int - Código numérico único que identifica o Exercicio (questão).
- McCabe’s complexity (métricas de complexidade):
    - `complexity`: float - __Complexidade Ciclomática__ Total.
    - `n_classes`: int - Número de __Classes__ declaradas no código do estudante.
    - `n_functions`: int - Número de __Funções__ declaradas no código do estudante.
- Raw metrics (métricas de código):
    - `loc`: int - Número Total de __Linhas de Código__.
    - `lloc`: int - Número Total de __Linhas Lógicas de Código__.
    - `sloc`: int - Número de Linhas de __Código Fonte__.
    - `single_comments`: int - Número de __Comentários__.
    - `comments`: int - Número de Linhas de __Docstrings__.
    - `multilines`: int - Número de __Multi-line strings__.
    - `black_lines`: int - Número de __Linhas em branco__.
- Halstead metrics (métricas de software):
    - `h1`: int - Número de __Operadores Distintos__.
    - `h2`: int - Número de __Operandos Distintos__.
    - `N1`: int - Número __Total de Operadores__.
    - `N2`: int - Número __Total de Operandos__.
    - `vocabulary`: int - __Vocabulário__ (`h = h1 + h2`).
    - `length`: int - __Tamanho__ (`N = N1 + N2`).
    - `calculated_N`: float - __Tamanho Estimado/Calculado__ em Byte (`h1*log2(h1) + h2*log2(h2)`).
    - `volume`: float - __Volume__ (`V = N * log2(h)`).
    - `difficulty`: float - __Dificuldade de Entendimento__ (`D = h1/2 * N2/h2`).
    - `effort`: float - __Esforço de Implementação__ (`E = D * V`).
    - `time`: float - __Tempo de Implementação__ (`T = E / 18 segundos`).
    - `bugs`: float - __Estimativa de Bugs/Erros__ na implementação (`B = V / 3000`).
- Tokens (obtidos do código fonte):
    - `imports`: int - quantidade de __linhas de importação__
    - `assignments` int - quantidade total de __operações de atribuição__ (incluindo atribuição combinada com outros operadores)
    - `assignments_unique`: int - quantidade de __operadores de atribuição distintos__
    - `kwds`: int - quantidade total de __keywords__
    - `kwds_unique`: int - quantidade de __keywords distintas__
    - `lt_numbers`: int - quantidade de __constantes numéricas__
    - `lt_strs`: int - quantidade de __constantes de texto (strings)__
    - `lt_bools`: int - quantidade de __constantes booleanas__
    - `lgc_op`: int - quantidade total de __operadores lógicos__
    - `lgc_op_unique`: int - quantidade de __operadores lógicos distintos__
    - `and_op`: int - quantidade total do __operador lógico 'and'__
    - `or_op`: int - quantidade total do __operador lógico 'or'__
    - `not_op`: int - quantidade total do __operador lógico 'not'__
    - `arithmetic_op`: int - quantidade total de __operadores aritméticos__
    - `arithmetic_op_unique`: int - quantidade de __operadores aritméticos distintos__
    - `add_op`: int - quantidade total do __operador adição '+'__
    - `minus_op`: int - quantidade total do __operador substração '-'__
    - `mult_op`: int - quantidade total do __operador multiplicação '*'__
    - `div_op`: int - quantidade total do __operador divisão ponto-flutuante '/'__
    - `mod_op`: int - quantidade total do __operador módulo '%'__
    - `power_op`: int - quantidade total do __operador potência '**'__
    - `div_floor_op`: int - quantidade total do __operador divisão inteira '//'__
    - `cmp_op`: int - quantidade total de __operadores relacionais__
    - `cmp_op_unique`: int - quantidade de __operadores relacionais distintos__
    - `equal_op`: int - quantidade total do __operador igualdade '=='__
    - `not_eq_op`: int - quantidade total do __operador desigualdade '!='__
    - `le_op`: int - quantidade total do __operador menor ou igual que '<='__
    - `ge_equal_op`: int - quantidade total do __operador maior ou igual que '>='__
    - `lt_op`: int - quantidade total do __operador menor que '<'__
    - `gt_op`: int - quantidade total do __operador maior que '>'__
    - `bitwise_op`: int - quantidade total de __operadores bit-a-bit__
    - `bitwise_op_unique`: int - quantidade de __operadores bit-a-bit distintos__
    - `bitwise_and`: int - quantidade total do __operador bit-a-bit and '&'__
    - `bitwise_or`: int - quantidade total do __operador bit-a-bit or '|'__
    - `bitwise_xor`: int - quantidade total do __operador bit-a-bit xor '^'__
    - `bitwise_not`: int - quantidade total do __operador bit-a-bit not (comp) '~'__
    - `lshift_op`: int - quantidade total do __operador left shift '<<'__
    - `rshift_op`: int - quantidade total do __operador right shift '>>'__
    - `identity_op`: int - quantidade total do __operador is__
    - `membership_op`: int - quantidade total do __operador in__
    - `conditionals`: int - quantidade total de __estruturas condicionais__ (if, elif, else)
    - `ifs`: int - quantidade total de __if's__
    - `elifs`: int - quantidade total de __elif's__
    - `elses`: int - quantidade total de __else's__
    - `loops`: int - quantidade total de __estruturas de repetição__ (while, for)
    - `whiles`: int - quantidade total de __while's__
    - `fors`: int - quantidade total de __for's__
    - `breaks`: int -  quantidade de __break's__
    - `continues`: int -  quantidade de __continue's__
    - `builtin_f`: int - quantidade total de __built-in functions__
    - `builtin_f_unique`: int - quantidade de __built-in functions__ distintas
    - `type_f`: int - quantidade total de funções de __casting/tipo__ (list, tuple, str, int, float ...)
    - `type_f_unique`: int - quantidade de funções de __tipo distintas__
    - `lambdas`: int - quantidade de __lambda expressions__
    - `lpar`: int - quantidade total de __(__
    - `rpar`: int - quantidade total de __)__
    - `lsqb`: int - quantidade total de __[__
    - `rsqb`: int - quantidade total de __]__
    - `lbrace`: int - quantidade total de __{__
    - `rbrace`: int - quantidade total de __}__
    - `commas`: int - quantidade total de __,__
    - `colons`: int - quantidade total de __:__
    - `dots`: int - quantidade total de __.__
    - `prints`: int - quantidade total de ocorrências da função __print (saídas)__
    - `inputs`: int - quantidade total de ocorrências da função __input (entradas)__
    - `len`: int - quantidade total de ocorrências da função __len (tamanho de sequences)__
    - `uident`: int - quantidade total de __user identifiers__
    - `uident_unique`: int - quantidade de __user identifiers distintos__
    - `uident_mean`: float - proporção __user identifiers__ por __linhas de código com identifiers__
    - `uident_per_line`: float - proporção de __user identifiers__ por linhas de código (loc), (__quantidadelinhas de código com identifiers__
    - `uident_chars`: float - proporção de __caracteres nos nomes dos identificadores__

### Erros

O arquivo `erros.csv` armazena as informações dos tipos de erros cometidos pelos estudantes nas tentativas de solucionar questões:

- `periodo`: string - Descrição do Período (ano e número do semestre).
- `turma`: int - Código da Turma (Disciplina) que o Estudante estava matriculado.
- `atividade`: int - Código da Atividade que continha o Exercícios a ser resolvido.
- `estudante`: int - Código do Estudante que cometeu o erro.
- `exercicio`: int - Código do Exercício (questão).
- `tipo`: string - Tipo do erro. Segue a nomenclatura de erros do próprio interpretador Python.
- `ocorrencias`: int - Quantidade de vezes que o Estudante cometeu o erro para o Exercício.


## Tecnologias e módulos utilizados

### Python3

Todo código fonte foi escrito e testado usando `Python 3.8.5`.

### os

O modúlo `os` foi utilizado para análise da estrutura de diretórios, recuperação dos nomes de arquivos contidos nos diretórios, criação de diretório e obtenção do diretório de trabalho atual.

### keyword

O módulo `keyword` foi utilizado para contagem de `keywords` encontradas nos códigos de solução.

### re

O módulo `re` foi utilizadona construção de __expressões regulares__ para análise e busca de padrões nos arquivos de `log`.

### datetime

O módulo `datetime` foi utilizado para obtenção da data atual, manipulação de datas e cálculo de intervalos de tempo.

### radon

O módulo `radon` foi utilizado nara extração de métricas de engenharia de software e cálculo da complexidade ciclomática do código de solução.

### tokenize

O módulo `tokenize` foi utilizado para extração de tokens do código de solução.

### csv

O módulo `csv` foi utilizado para salvar as informações extraídas em arquivos.

### logging

O módulo `logging` foi utiliado para configuração e monitoramento do processo de execução do projeto, optou-se por arquivos de `log`.

## Contato

Marcos A. P. de Lima  – marcos.lima@icomp.ufam.edu.br
[![LinkedIn][linkedin-shield]][linkedin-url]

Prof. Leandro Silva Galvao de Carvalho – galvao@icomp.ufam.edu.br

<!-- ACKNOWLEDGEMENTS -->
## Agradecimentos

- Prof. David B. F. Oliveira
- Profª. Elaine H. T. Oliveira
- Prof. Filipe Dwan Pereira

## License

- **[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html)** [![GNU GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
- Copyright 2020 © [marcosmapl](https://github.com/marcosmapl).

<!-- Markdown link & img dfn's -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/marcosmapl