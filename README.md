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

O CodeBench é um Juiz Online de Programação criado pelo Instituto de Computação da Universidade Federal do Amazonas, Brasil. Ele permite que professores disponibilizem listas de exercícios de programação para os alunos, que devem desenvolver soluções por meio de uma IDE integrada. Ao submeter o código-fonte de um exercício, o aluno recebe imediatamente um feedback sobre a correção da solução. Todas as ações dos alunos na IDE são registradas automaticamente pelo CodeBench, e este dataset contém os logs de estudantes de CS1 de 2016 a 2021. Para mais detalhes, visite [CodeBench](http://codebench.icomp.ufam.edu.br).

Uma vez que um aluno submete uma solução para um dado exercício, o sistema informa instantaneamente ao aluno se sua solução está correta ou errada. As soluções são verificadas por meio de casos de teste. Ao cadastrar um dado exercício no sistema, o professor ou monitor deverá informar um ou mais casos de testes que serão usados para julgar a corretude dos códigos submetidos pelos alunos.

Atualmente, o CodeBench suporta as seguintes linguagens de programação: C, C++, Java, Python, Haskell e Lua. Além dessas linguagens, o ambiente também suporta a linguagem SQL, para exercícios envolvendo consultas a bancos de dados. Ao criar um dado trabalho, o professor ou monitor deverá informar qual linguagem será usada pelos alunos para desenvolver as soluções dos exercícios de programação desse trabalho. Além disso, o CodeBench permite a troca de mensagens entre alunos e professores de uma dada turma, bem como o compartilhamento de recursos didáticos por parte dos professores.

### Dataset

O CodeBench registra automaticamente todas as ações realizadas pelos alunos no IDE incorporado durante suas tentativas de resolver os exercícios propostos. Atualmente o conjunto de dados contém todos os registros coletados de alunos CS1 durante os semestres letivos compreendidos entre 2016 e 2019. Os dados estão distribuídos em diversos arquivos, organizados numa estrutura hierárquica de diretórios.

Devido a organização semi-estruturada e distribuída dos dados, fez-se necessário organizá-los segundo algum critério. Para tanto, desenvolvemos em Python um extrator automatizado, capaz de percorrer todo o conjunto de dados, minerando e organizando as informações disponíveis. Mais informações sobre o dataset podem ser obtidas em: http://codebench.icomp.ufam.edu.br/dataset/

### Estrutura do projeto

O projeto está organizado segundo a estrutura abaixo:

```
codebench-mining-tool
└─── main.py
└─── model.py
└─── util.py
└─── requirements.txt
│ LICENSE
│ README.md
```
#### Main

O arquivo `main.py` é o ponto de entrada do projeto, e por isso deve ser executado usando o interpretador Python. Ele recebe os caminho para o dataset já previamente descompactado por meio do argumento de linha de comando `-ds`, para que o extrator possa fazer uma varredura em toda a estrutura de pastas, identificando `períodos`, `turmas`, `atividades`, `usários`, `execuções` e `soluções`. Os argumentos aceitos pelo script são:

- `-ds` ou `--dataset`: Caminho para a pasta com o dataset já descompactado.
- `--executions` | `--no-executions`: Indica se as informações referentes às execuções de código feitas pelos estudantes durante a resolução de questões devem ser extraídas. Por padrão não serão extraídas (`--no-executions`).
- `--solutions` | `--no-solutions`: Indica se as informações referentes aos códigos de solução elaborados pelos estudantes durante a resolução de questões devem ser extraídas. Por padrão não serão extraídas (`--no-executions`).
- `--logins` | `--no-logins`: Indica se as informações referentes aos logins efetuados pelos estudantes devem ser extraídas. Por padrão não serão extraídas (`--no-logins`).
- `--grades` | `--no-grades`: Indica se as informações referentes às notas obtidas pelos estudantes nas atividades devem ser extraídas. Por padrão não serão extraídas (`--no-grades`).
- `--codemirror` | `--no-codemirror`: Indica se as informações contidas nos logs do editor de texto (codemirror) utilizado pelos estudantes na resolução das questões devem ser extraídas. Por padrão não serão extraídas (`--no-codemirror`).

#### Model

O arquivo `model.py` contem a declaração de todas as classes de modelo de dados (entidades) utilizadas pelo extrator, e que posteriormente serão salvas em arquivos `.csv`. Essas entidades são:

- `CodebenchObject`: interface que expões métodos para objetos (entidade) que serão salvas em arquivos `.csv`.
- `Semester`: classe para objetos que representam os períodos letivos.
- `Course`: classe para objetos que representam as turmas de estudantes num período letivo.
- `Assignment`: classe para objetos que representam as atividades realizada numa turma.
- `User`: classe para objetos que representam os usuários (estudantes) matrículados numa turma.
- `Execution`: classe para objetos que sumarizam as informações coletadas durante a tentativa de um estudante solucionar uma questão.
- `SolutionMetrics`: classe para objetos que sumarizam as métricas extraídas da solução de um usuário (estudante) para uma questão.
- `Login`: classe que representa um evento de login/logout do usuário (estudante).
- `CodeMirror`: classe que representar um evento de interação do usuário (estudante) com o editor de código.
- `Grade`: classe que representa o desempenho de um usuário (estudante) numa atividade.

#### Util

O arquivo `util.py` contem a declaração de variáveis, constantes e funções todos utilizados na extração das informações do dataset. Além disso a classe `Logger` também é implementada. Essa classe é reponsável pelo gerenciamento dos `logs` gerados pelo extrator. As informações um resumo de quais informações puderam ser extraídas e também registro de erros ocorridos durante o processo de extração são armazenados em arquivos de `log`. Os arquivos são salvos por padrão na pasta `logs`, criada na raiz do projeto. A cada execução são gerados três arquivos de `log` inciados pela data e hora de execução do extrator:

- `<data_hoje>_info.log`: registra cada entidade encontrada pelo extrator.
- `<data_hoje>_warn.log`: registra avisos de eventos não esperados durante a extração (ausência do código de solução ou arquivo corrompido, por exemplo).
- `<data_hoje>_error.log`: registra as falhas ocorridas durante a extração. Em geral essas falhas são ocorridas na etapa de extração de métricas dos códigos de solução. Alguns destes códigos podem ser incompletos, gerando problemas para as bibliotecas de extração de métricas.

#### Dependências

O arquivo `requirements.txt` pode ser utilizado junto com o `pip` para instalar as dependências do projeto.

	pip install -U -r requirements.txt

 	-U: atualiza as dependências se já estiverem instaladas.
  	-r: arquivo com as dependências requeridas.

#### Exemplo de uso

Extraindo somente informações básiscas (períodos letivos, turmas, atividades e usuários): 
		
  	python3 main.py -ds home/Documents/cb_dataset_2023_1_v1.8
	
Extraindo informações básicas e também as execuções: 

  	python3 main.py -ds home/Documents/cb_dataset_2023_1_v1.8 --executions
	
Extraindo informações básicas e também as soluções: 

  	python3 main.py -ds home/Documents/cb_dataset_2023_1_v1.8 --solutions
	
Extraindo informações básicas e também as notas: 

  	python3 main.py -ds home/Documents/cb_dataset_2023_1_v1.8 --grades
	
Extraindo informações básicas e também os eventos de logins: 

  	python3 main.py -ds home/Documents/cb_dataset_2023_1_v1.8 --logins
	
Extraindo informações básicas e também os eventos do CodeMirror: 

  	python3 main.py -ds home/Documents/cb_dataset_2023_1_v1.8 --codemirror

## Arquivos de saída

As informações extraídas do dataset são estruturadas em arquivos `csv`.

### Períodos

Os arquivo `semesters.csv` armazena das informações extraídas de todos os períodos letivos registrados:

- `desc` (str): Uma string descrevendo o semestre.
- `n_courses` (int): O número de cursos no semestre.
- `n_assignments` (int): O número de atribuições no semestre.
- `n_users` (int): O número de usuários associados ao semestre.
- `n_codes` (int): O número de códigos de usuários associados ao semestre.
- `n_executions_files` (int): O número de arquivos de log de execução do usuário no semestre.
- `n_executions` (int): O número de execuções de usuários (submissões ou testes) no semestre.
- `n_mirror_files` (int): O número de arquivos de log de espelhamento de código no semestre.
- `n_mirror_events` (int): O número de eventos de espelhamento de código no semestre.
- `n_login_files` (int): O número de arquivos de log de login no semestre.
- `n_login_events` (int): O número de eventos de login/logout no semestre.
- `n_grades` (int): O número de notas dos usuários associadas ao semestre.

### Turmas

Os arquivo `courses.csv` armazena das informações extraídas de todas turmas registradas:

- `semester` (str): O período letivo ou semestre ao qual o curso (disciplina) pertence.
- `code` (str): O código ou identificador do curso (disciplina).
- `desc` (str): Descrição do curso (disciplina).
- `n_assignments` (int): Número de atividades associadas ao curso (disciplina).
- `n_users` (int): Número de usuários matriculados no curso (disciplina).

### Atividades

Os arquivo `assignments.csv` armazena das informações extraídas de todas as atividades realizadas:

- `semester` (str): O período letivo durante o qual a atividade é realizada.
- `course` (str): O curso (disciplina) ao qual a atividade pertence.
- `code` (str): Identificador único para a atividade.
- `title` (str ou None): O título da atividade.
- `open_date` (str ou None): A data em que a atividade é aberta.
- `close_date` (str ou None): A data em que a atividade é fechada.
- `programming_lang` (str ou None): A linguagem de programação usada para a atividade.
- `assignment_type` (str ou None): O tipo de atividade (por exemplo, lição de casa, exame).
- `weight` (float ou None): O peso/importância da atividade.
- `n_blocks` (int ou None): O número de blocos de problemas na atividade.
- `blocks` (lista): Uma lista contendo os blocos de problemas para a atividade.

### Estudantes

Os arquivo `users.csv` armazena das informações extraídas de todos os estudantes registrados:

- `semestre` (str): O período letivo.
- `course` (str): O nome do curso (disciplina) em que o usuário está matriculado.
- `code` (str): Um código identificador único para o usuário.
- `course_id` (str): O identificador único para o curso de graduação.
- `course_name` (str): O nome do curso de gradução.
- `institution_id` (str): O identificador único para a instituição.
- `institution_name` (str): O nome da instituição.
- `high_school_name` (str): O nome da escola secundária frequentada pelo usuário.
- `school_type` (str): O tipo de escola secundária (por exemplo, pública, privada).
- `shift` (str): O turno em que o usuário frequentou a escola secundária.
- `graduation_year` (int): O ano em que o usuário se formou no ensino médio.
- `has_a_pc` (bool): Se o usuário tem um computador pessoal.
- `share_this_pc` (bool): Se o usuário compartilha seu computador pessoal.
- `this_pc_has` (str): Especificações ou características do computador pessoal do usuário.
- `previous_experience_of` (str): Experiência anterior do usuário no campo.
- `worked_or_interned` (bool): Se o usuário trabalhou ou estagiou.
- `company_name` (str): O nome da empresa onde o usuário trabalhou ou estagiou.
- `year_started_working` (int): O ano em que o usuário começou a trabalhar.
- `year_stopped_working` (int): O ano em que o usuário parou de trabalhar.
- `started_other_degree` (bool): Se o usuário iniciou outro curso.
- `degree_course` (str): O nome do outro curso de graduação.
- `institution_name_2` (str): O nome da instituição do outro curso.
- `year_started_this` (int): O ano em que o usuário iniciou o outro curso.
- `year_stopped_this` (int): O ano em que o usuário parou o outro curso.
- `sex` (str): O sexo do usuário.
- `year_of_birth` (int): O ano de nascimento do usuário.
- `civil_status` (str): O estado civil do usuário (por exemplo, solteiro, casado).
- `have_kids` (bool): Se o usuário tem filhos.

### Execuções

O arquivo `executions.csv` armazena as informações extraídas dos arquivos de logs de tentativas dos estudantes durante a tentativa de solucionar um problema de programação.

- `semestre` (str): O semestre durante o qual ocorreu o evento de login.
- `course` (str): O curso associado ao evento de login.
- `assignment` (str): A tarefa do curso.
- `user` (str): O identificador único do usuário.
- `problem` (str): O identificador do problema.
- `seq` (int): A ordem sequencial de execução.
- `tipo_ex` (str): O tipo de execução (Submissão | Teste).
- `data_hora` (str): A data e hora da execução.

Métricas de complexidade:
  
- `complexity` (float): Medição de complexidade, se disponível.
- `n_classes` (int): Número de classes, se disponível.
- `n_functions` (int): Número de funções, se disponível.
- `funcs_complexity` (float): Complexidade das funções, se disponível.
- `classes_complexity` (float): Complexidade das classes, se disponível.
- `total_complexity` (float): Complexidade total, se disponível.
- `n_blocks` (int): Número de blocos, se disponível.
- `loc` (int): Linhas de código, se disponível.
- `lloc` (int): Linhas de código lógicas, se disponível.
- `sloc` (int): Linhas de código fonte, se disponível.
- `comments` (int): Número de comentários, se disponível.
- `single_comments` (int): Número de comentários de uma linha, se disponível.
- `multi_comments` (int): Número de comentários de múltiplas linhas, se disponível.
- `blank_lines` (int): Número de linhas em branco, se disponível.

Métricas de Halstead:

- `h1` (int): Métrica de Halstead h1, se disponível.
- `h2` (int): Métrica de Halstead h2, se disponível.
- `N1` (int): Métrica de Halstead N1, se disponível.
- `N2` (int): Métrica de Halstead N2, se disponível.
- `vocabulary` (int): Métrica de Halstead h, se disponível.
- `length` (int): Métrica de Halstead N, se disponível.
- `calculated_length` (int): Métrica de Halstead N calculada, se disponível.
- `volume` (int): Volume de Halstead, se disponível.
- `difficulty` (float): Dificuldade de Halstead, se disponível.
- `effort`  (float): Esforço de Halstead, se disponível.
- `bugs` (int): Bugs de Halstead, se disponível.
- `time` (float): Tempo de Halstead, se disponível.

Métricas baseadas em operadores:

- `endmarker` (int): Marcador de fim de código, se disponível.
- `name` (int): Nomes literais no código, se disponível.
- `number` (int): Números literais no código, se disponível.
- `string` (int): Strings literais no código, se disponível.
- `newline` (int): Quebras de linha de código, se disponível.
- `indent` (int): Indentações de código, se disponível.
- `dedent` (int): Dedentações de código, se disponível.
- `lpar` (int): Número de parênteses esquerdos, se disponível.
- `rpar` (int): Número de parênteses direitos, se disponível.
- `lsqb` (int): Número de colchetes esquerdos, se disponível.
- `rsqb` (int): Número de colchetes direitos, se disponível.
- `colon` (int): Número de dois pontos, se disponível.
- `comma` (int): Número de vírgulas, se disponível.
- `semi` (int): Número de ponto e vírgulas, se disponível.
- `plus` (int): Número de sinais de adição, se disponível.
- `minus` (int): Número de sinais de subtração, se disponível.
- `star` (int): Número de asteriscos, se disponível.
- `slash` (int): Número de barras, se disponível.
- `vbar` (int): Número de barras verticais, se disponível.
- `amper` (int): Número de símbolos de "e" lógico, se disponível.
- `less` (int): Número de sinais de menor que, se disponível.
- `greater` (int): Número de sinais de maior que, se disponível.
- `equal` (int): Número de sinais de igual, se disponível.
- `dot` (int): Número de pontos, se disponível.
- `percent` (int): Número de sinais de porcentagem, se disponível.
- `lbrace` (int): Número de chaves esquerdas, se disponível.
- `rbrace` (int): Número de chaves direitas, se disponível.
- `eq_equal` (int): Número de operadores de igualdade, se disponível.
- `not_eq` (int): Número de operadores de desigualdade, se disponível.
- `less_eq` (int): Número de operadores de menor ou igual, se disponível.
- `greater_eq` (int): Número de operadores de maior ou igual, se disponível.
- `tilde` (int): Número de símbolos de til, se disponível.
- `circumflex` (int): Número de símbolos de circunflexo, se disponível.
- `lshift` (int): Número de operadores de deslocamento à esquerda, se disponível.
- `rshift` (int): Número de operadores de deslocamento à direita, se disponível.
- `dbl_star` (int): Número de operadores de duplo asterisco, se disponível.
- `plus_eq` (int): Número de operadores de adição e atribuição, se disponível.
- `minus_eq` (int): Número de operadores de subtração e atribuição, se disponível.
- `star_eq` (int): Número de operadores de multiplicação e atribuição, se disponível.
- `slash_eq` (int): Número de operadores de divisão e atribuição, se disponível.
- `percent_eq` (int): Número de operadores de porcentagem e atribuição, se disponível.
- `amper_eq` (int): Número de operadores de "e" lógico e atribuição, se disponível.
- `vbar_eq` (int): Número de operadores de barra vertical e atribuição, se disponível.
- `circumflex_eq` (int): Número de operadores de circunflexo e atribuição, se disponível.
- `lshift_eq` (int): Número de operadores de deslocamento à esquerda e atribuição, se disponível.
- `rshift_eq` (int): Número de operadores de deslocamento à direita e atribuição, se disponível.
- `dbl_star_eq` (int): Número de operadores de dupla estrela e atribuição, se disponível.
- `dbl_slash` (int): Número de operadores de barra dupla, se disponível.
- `dbl_slash_eq` (int): Número de operadores de barra dupla e atribuição, se disponível.
- `at` (int): Número de operadores de arroba, se disponível.
- `at_eq` (int): Número de operadores de arroba e atribuição, se disponível.
- `rarrow` (int): Número de operadores de seta direita, se disponível.
- `ellipsis` (int): Número de operadores de reticências, se disponível.
- `colon_eq` (int): Número de operadores de dois pontos e atribuição, se disponível.
- `op` (int): Número total de operadores.

Métricas baseadas em Tokens:

- `error_token` (int): Número de tokens de erro, se disponível.
- `comment` (int): Número de comentários, se disponível.
- `nl` (int): Número de novas linhas disponíveis.
- `encoding` (int): Número de comandos de codificação, se disponível.
- `number_int` (int): Número de funções int, se disponível.
- `number_float` (int): Número de funções float, se disponível.
- `kwd_and` (int): Número de operadores and, se disponível.
- `kwd_or` (int): Número de operadores or, se disponível.
- `kwd_not` (int): Número de operadores not, se disponível.
- `kwd_none` (int): Número de palavras-chave none, se disponível.
-  `kwd_false` (int): Número de palavras-chave false, se disponível.
- `kwd_true` (int): Número de palavras-chave true, se disponível.
- `kwd_as` (int): Número de palavras-chave as, se disponível.
- `kwd_assert` (int): Número de funções assert, se disponível.
- `kwd_async` (int): Número de operadores async, se disponível.
- `kwd_await` (int): Número de operadores await, se disponível.
- `kwd_break` (int): Número de operadores break, se disponível.
- `kwd_class` (int): Número de palavras-chave class, se disponível.
- `kwd_continue` (int): Número de operadores continue, se disponível.
- `kwd_def` (int): Número de palavras-chave def, se disponível.
- `kwd_del` (int): Número de operadores del, se disponível.
- `kwd_if` (int): Número de palavras-chave if, se disponível.
- `kwd_elif` (int): Número de palavras-chave elif, se disponível.
- `kwd_else` (int): Número de palavras-chave else, se disponível.
- `kwd_except` (int): Número de palavras-chave except, se disponível.
- `kwd_finally` (int): Número de palavras-chave finally, se disponível.
- `kwd_for` (int): Número de palavras-chave for, se disponível.
- `kwd_while` (int): Número de palavras-chave while, se disponível.
- `kwd_import` (int): Número de palavras-chave import, se disponível.
- `kwd_from` (int): Número de palavras-chave from, se disponível.
- `kwd_global` (int): Número de palavras-chave global, se disponível.
- `kwd_in` (int): Número de palavras-chave in, se disponível.
- `kwd_is` (int): Número de palavras-chave is, se disponível.
- `kwd_lambda` (int): Número de palavras-chave lambda, se disponível.
- `kwd_nonlocal` (int): Número de palavras-chave nonlocal, se disponível.
- `kwd_pass` (int): Número de palavras-chave pass, se disponível.
- `kwd_raise` (int): Número de palavras-chave raise, se disponível.
- `kwd_return` (int): Número de palavras-chave return, se disponível.
- `kwd_try` (int): Número de palavras-chave try, se disponível.
- `kwd_with` (int): Número de palavras-chave with, se disponível.
- `kwd_yield` (int): Número de palavras-chave yield, se disponível.
- `keyword` (int): Número de palavras-chave, se disponível.
- `identifier` (int): Número de identificadores, se disponível.
- `builtin_type` (int): Número de tipos integrados, se disponível.
- `builtin_func` (int): Número de funções integradas, se disponível.
- `kwd_print` (int): Número de prints, se disponível.
- `kwd_input` (int): Número de inputs, se disponível.
- `builtin_type_unique` (int): Número de tipos integrados únicos, se disponível.
- `builtin_func_unique` (int): Número de funções integradas únicas, se disponível.
- `identifiers_unique` (int): Número de identificadores únicos, se disponível.
- `identifiers_max_len` (int): Comprimento máximo dos identificadores, se disponível.
- `identifiers_min_len` (int): Comprimento mínimo dos identificadores, se disponível.
- `identifiers_mean_len` (float): Comprimento médio dos identificadores, se disponível.

### Soluções

O arquivo `solutions.csv` armazena as informações extraídas dos códigos de solução elaborados pelos usuários (estudantes) e que ficam na pasta `codes`.

- `semester` (str): O período letivo.
- `course` (str): O código do curso (disciplina).
- `assignment` (str): O código da atividade.
- `user` (str): O código do usuário.
- `problem` (str): O código do problema.

Métricas de complexidade:
  
- `complexity` (float): Medição de complexidade, se disponível.
- `n_classes` (int): Número de classes, se disponível.
- `n_functions` (int): Número de funções, se disponível.
- `funcs_complexity` (float): Complexidade das funções, se disponível.
- `classes_complexity` (float): Complexidade das classes, se disponível.
- `total_complexity` (float): Complexidade total, se disponível.
- `n_blocks` (int): Número de blocos, se disponível.
- `loc` (int): Linhas de código, se disponível.
- `lloc` (int): Linhas de código lógicas, se disponível.
- `sloc` (int): Linhas de código fonte, se disponível.
- `comments` (int): Número de comentários, se disponível.
- `single_comments` (int): Número de comentários de uma linha, se disponível.
- `multi_comments` (int): Número de comentários de múltiplas linhas, se disponível.
- `blank_lines` (int): Número de linhas em branco, se disponível.

Métricas de Halstead:

- `h1` (int): Métrica de Halstead h1, se disponível.
- `h2` (int): Métrica de Halstead h2, se disponível.
- `N1` (int): Métrica de Halstead N1, se disponível.
- `N2` (int): Métrica de Halstead N2, se disponível.
- `vocabulary` (int): Métrica de Halstead h, se disponível.
- `length` (int): Métrica de Halstead N, se disponível.
- `calculated_length` (int): Métrica de Halstead N calculada, se disponível.
- `volume` (int): Volume de Halstead, se disponível.
- `difficulty` (float): Dificuldade de Halstead, se disponível.
- `effort`  (float): Esforço de Halstead, se disponível.
- `bugs` (int): Bugs de Halstead, se disponível.
- `time` (float): Tempo de Halstead, se disponível.

Métricas baseadas em operadores:

- `endmarker` (int): Marcador de fim de código, se disponível.
- `name` (int): Nomes literais no código, se disponível.
- `number` (int): Números literais no código, se disponível.
- `string` (int): Strings literais no código, se disponível.
- `newline` (int): Quebras de linha de código, se disponível.
- `indent` (int): Indentações de código, se disponível.
- `dedent` (int): Dedentações de código, se disponível.
- `lpar` (int): Número de parênteses esquerdos, se disponível.
- `rpar` (int): Número de parênteses direitos, se disponível.
- `lsqb` (int): Número de colchetes esquerdos, se disponível.
- `rsqb` (int): Número de colchetes direitos, se disponível.
- `colon` (int): Número de dois pontos, se disponível.
- `comma` (int): Número de vírgulas, se disponível.
- `semi` (int): Número de ponto e vírgulas, se disponível.
- `plus` (int): Número de sinais de adição, se disponível.
- `minus` (int): Número de sinais de subtração, se disponível.
- `star` (int): Número de asteriscos, se disponível.
- `slash` (int): Número de barras, se disponível.
- `vbar` (int): Número de barras verticais, se disponível.
- `amper` (int): Número de símbolos de "e" lógico, se disponível.
- `less` (int): Número de sinais de menor que, se disponível.
- `greater` (int): Número de sinais de maior que, se disponível.
- `equal` (int): Número de sinais de igual, se disponível.
- `dot` (int): Número de pontos, se disponível.
- `percent` (int): Número de sinais de porcentagem, se disponível.
- `lbrace` (int): Número de chaves esquerdas, se disponível.
- `rbrace` (int): Número de chaves direitas, se disponível.
- `eq_equal` (int): Número de operadores de igualdade, se disponível.
- `not_eq` (int): Número de operadores de desigualdade, se disponível.
- `less_eq` (int): Número de operadores de menor ou igual, se disponível.
- `greater_eq` (int): Número de operadores de maior ou igual, se disponível.
- `tilde` (int): Número de símbolos de til, se disponível.
- `circumflex` (int): Número de símbolos de circunflexo, se disponível.
- `lshift` (int): Número de operadores de deslocamento à esquerda, se disponível.
- `rshift` (int): Número de operadores de deslocamento à direita, se disponível.
- `dbl_star` (int): Número de operadores de duplo asterisco, se disponível.
- `plus_eq` (int): Número de operadores de adição e atribuição, se disponível.
- `minus_eq` (int): Número de operadores de subtração e atribuição, se disponível.
- `star_eq` (int): Número de operadores de multiplicação e atribuição, se disponível.
- `slash_eq` (int): Número de operadores de divisão e atribuição, se disponível.
- `percent_eq` (int): Número de operadores de porcentagem e atribuição, se disponível.
- `amper_eq` (int): Número de operadores de "e" lógico e atribuição, se disponível.
- `vbar_eq` (int): Número de operadores de barra vertical e atribuição, se disponível.
- `circumflex_eq` (int): Número de operadores de circunflexo e atribuição, se disponível.
- `lshift_eq` (int): Número de operadores de deslocamento à esquerda e atribuição, se disponível.
- `rshift_eq` (int): Número de operadores de deslocamento à direita e atribuição, se disponível.
- `dbl_star_eq` (int): Número de operadores de dupla estrela e atribuição, se disponível.
- `dbl_slash` (int): Número de operadores de barra dupla, se disponível.
- `dbl_slash_eq` (int): Número de operadores de barra dupla e atribuição, se disponível.
- `at` (int): Número de operadores de arroba, se disponível.
- `at_eq` (int): Número de operadores de arroba e atribuição, se disponível.
- `rarrow` (int): Número de operadores de seta direita, se disponível.
- `ellipsis` (int): Número de operadores de reticências, se disponível.
- `colon_eq` (int): Número de operadores de dois pontos e atribuição, se disponível.
- `op` (int): Número total de operadores.

Métricas baseadas em Tokens:

- `error_token` (int): Número de tokens de erro, se disponível.
- `comment` (int): Número de comentários, se disponível.
- `nl` (int): Número de novas linhas disponíveis.
- `encoding` (int): Número de comandos de codificação, se disponível.
- `number_int` (int): Número de funções int, se disponível.
- `number_float` (int): Número de funções float, se disponível.
- `kwd_and` (int): Número de operadores and, se disponível.
- `kwd_or` (int): Número de operadores or, se disponível.
- `kwd_not` (int): Número de operadores not, se disponível.
- `kwd_none` (int): Número de palavras-chave none, se disponível.
-  `kwd_false` (int): Número de palavras-chave false, se disponível.
- `kwd_true` (int): Número de palavras-chave true, se disponível.
- `kwd_as` (int): Número de palavras-chave as, se disponível.
- `kwd_assert` (int): Número de funções assert, se disponível.
- `kwd_async` (int): Número de operadores async, se disponível.
- `kwd_await` (int): Número de operadores await, se disponível.
- `kwd_break` (int): Número de operadores break, se disponível.
- `kwd_class` (int): Número de palavras-chave class, se disponível.
- `kwd_continue` (int): Número de operadores continue, se disponível.
- `kwd_def` (int): Número de palavras-chave def, se disponível.
- `kwd_del` (int): Número de operadores del, se disponível.
- `kwd_if` (int): Número de palavras-chave if, se disponível.
- `kwd_elif` (int): Número de palavras-chave elif, se disponível.
- `kwd_else` (int): Número de palavras-chave else, se disponível.
- `kwd_except` (int): Número de palavras-chave except, se disponível.
- `kwd_finally` (int): Número de palavras-chave finally, se disponível.
- `kwd_for` (int): Número de palavras-chave for, se disponível.
- `kwd_while` (int): Número de palavras-chave while, se disponível.
- `kwd_import` (int): Número de palavras-chave import, se disponível.
- `kwd_from` (int): Número de palavras-chave from, se disponível.
- `kwd_global` (int): Número de palavras-chave global, se disponível.
- `kwd_in` (int): Número de palavras-chave in, se disponível.
- `kwd_is` (int): Número de palavras-chave is, se disponível.
- `kwd_lambda` (int): Número de palavras-chave lambda, se disponível.
- `kwd_nonlocal` (int): Número de palavras-chave nonlocal, se disponível.
- `kwd_pass` (int): Número de palavras-chave pass, se disponível.
- `kwd_raise` (int): Número de palavras-chave raise, se disponível.
- `kwd_return` (int): Número de palavras-chave return, se disponível.
- `kwd_try` (int): Número de palavras-chave try, se disponível.
- `kwd_with` (int): Número de palavras-chave with, se disponível.
- `kwd_yield` (int): Número de palavras-chave yield, se disponível.
- `keyword` (int): Número de palavras-chave, se disponível.
- `identifier` (int): Número de identificadores, se disponível.
- `builtin_type` (int): Número de tipos integrados, se disponível.
- `builtin_func` (int): Número de funções integradas, se disponível.
- `kwd_print` (int): Número de prints, se disponível.
- `kwd_input` (int): Número de inputs, se disponível.
- `builtin_type_unique` (int): Número de tipos integrados únicos, se disponível.
- `builtin_func_unique` (int): Número de funções integradas únicas, se disponível.
- `identifiers_unique` (int): Número de identificadores únicos, se disponível.
- `identifiers_max_len` (int): Comprimento máximo dos identificadores, se disponível.
- `identifiers_min_len` (int): Comprimento mínimo dos identificadores, se disponível.
- `identifiers_mean_len` (float): Comprimento médio dos identificadores, se disponível.

### Notas

O arquivo `grades.csv` armazena as informações das notas obtidas pelos usuários (estudantes) nas atividades:

- `semester` (str): O semestre letivo.
- `course` (str): O código do curso (disciplina.
- `assignment` (str): O código da atividade.
- `user` (str): O código do usuários (estudante).
- `grade` (float): A nota obtida na atividade.
- `n_problems` (int):Número de problemas na atividade.
- `n_correct` (int): Número de problemas solucionados pelo usuário (estudante).
- `n_wrong` (int): Número de problemas não solucionados pelo usuários (estudante).
- `n_blank` (int): Número de problemas deixados em bracno pelo usuários (estudante).

### Logins

O arquivo `logins.csv` armazena as informações dos eventos de login/logout dos usuários:

- `semester` (str): O período letivo.
- `course` (str): O código do curso (disciplina).
- `date` (str): A data do evento.
- `time` (str): O horário do evento.
- `user` (str): O código do usuário.
- `event` (str): O tipo de evento (i.e., "login", "logout").

### CodeMirror

O arquivo `mirrors.csv` armazena as informações dos eventos de login/logout dos usuários:

- `semester` (str): O período letivo.
- `course` (str): O código do curso (disciplina).
- `assignment` (str): O código da atividade.
- `user` (str): O código do usuários (estudante).
- `problem` (str): O código do problema.
- `timestamp` (str): O timestamp do evento (em milisegundos).
- `date` (str): A data do evento.
- `time` (str): O horário do evento.
- `event` (str): O tipo do evento.
- `msg` (str): Mensagem adicional relacionada ao evento.

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

### Pendas

O módulo `pandas.DataFrame` foi utilizado para salvar as informações extraídas em arquivos `.csv`.

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
