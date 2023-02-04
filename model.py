# -*- coding: utf-8 -*-
### Codebench Dataset Extractor by Marcos Lima (marcos.lima@icomp.ufam.edu.br)
### Universidade Federal do Amazonas - UFAM
### Instituto de Computação - IComp


class Entidade:
    """Interface que especifica os métodos de uma Entidade que possa ser salva num arquivo '.csv' (dataset)."""

    def as_list(self):
        """Retorna valores dos atributos da Entidade numa lista (row), para então serem salvos no dataset."""
        pass

    @staticmethod
    def get_lista_atributos():
        """Retorna uma lista com o nome de todos os atributos da Entidade, que devam ser salvas no dataset (csv file header)."""
        pass


class Periodo(Entidade):
    """Entidade que representa um Período letivo."""

    def __init__(self, descricao, n_turmas, n_atividades, n_estudantes, n_codes, n_tentativas, n_cmirrors, n_grades, n_mousemoves, path):
        self.descricao = descricao
        self.n_turmas = n_turmas
        self.n_atividades = n_atividades
        self.n_estudantes = n_estudantes
        self.n_codes = n_codes
        self.n_tentativas = n_tentativas
        self.n_cmirrors = n_cmirrors
        self.n_grades = n_grades
        self.n_mousemoves = n_mousemoves
        self.path = path
        self.turmas = []

    def as_list(self):
        return [
            self.descricao,
            self.n_turmas,
            self.n_atividades,
            self.n_estudantes,
            self.n_codes,
            self.n_tentativas,
            self.n_cmirrors,
            self.n_grades,
            self.n_mousemoves
        ]

    @staticmethod
    def get_lista_atributos():
        return list(Periodo(None, None, None, None, None, None, None, None, None, None).__dict__)[:-2]


class Turma(Entidade):
    """Entidade que representa uma Turma de Estudantes num :class:`Periodo` letivo."""

    def __init__(self, periodo, codigo, descricao, n_atividades, n_estudantes, path):
        self.periodo = periodo
        self.codigo = codigo
        self.descricao = descricao
        self.n_atividades = n_atividades
        self.n_estudantes = n_estudantes
        self.path = path

    def as_list(self):
        return [
            self.periodo,
            self.codigo,
            self.descricao,
            self.n_atividades,
            self.n_estudantes
        ]

    @staticmethod
    def get_lista_atributos():
        return list(Turma(None, None, None, None, None, None).__dict__)[:-1]


class Atividade(Entidade):
    """Entidade que representa uma Atividade realizada numa :class:`Turma`."""

    def __init__(self, periodo, turma, codigo, path):
        self.periodo = periodo
        self.turma = turma
        self.codigo = codigo
        self.titulo = None
        self.data_inicio = None
        self.data_termino = None
        self.linguagem = None
        self.tipo = None
        self.peso = None
        self.n_blocos = None
        self.blocos = []
        self.path = path

    def as_list(self):
        return [
            self.periodo,
            self.turma,
            self.codigo,
            self.titulo,
            self.data_inicio,
            self.data_termino,
            self.linguagem,
            self.tipo,
            self.peso,
            self.n_blocos,
            self.blocos
        ]

    @staticmethod
    def get_lista_atributos():
        return list(Atividade(None, None, None, None).__dict__)[:-1]


class Usuario(Entidade):
    """Entidade que representa um Estudante matriculado numa :class:`Turma`."""

    def __init__(self, periodo, turma, codigo, path):
        self.periodo = periodo
        self.turma = turma
        self.codigo = codigo
        self.curso_id = None
        self.curso_nome = None
        self.instituicao_id = None
        self.instituicao_nome = None
        self.escola_nome = None
        self.escola_tipo = None
        self.escola_turno = None
        self.escola_ano_grad = None
        self.computador = None
        self.computador_compartilhado = None
        self.internet = None
        self.programa = None
        self.trabalha = None
        self.empresa_nome = None
        self.trabalha_ano_inicio = None
        self.trabalha_ano_termino = None
        self.outra_graduacao = None
        self.outra_graduacao_curso = None
        self.outra_graduacao_ano_inicio = None
        self.outra_graduacao_ano_fim = None
        self.sexo = None
        self.ano_nascimento = None
        self.estado_civil = None
        self.filhos = None
        self.path = path

    def as_list(self):
        return [
            self.periodo,
            self.turma,
            self.codigo,
            self.curso_id,
            self.curso_nome,
            self.instituicao_id,
            self.instituicao_nome,
            self.escola_nome,
            self.escola_tipo,
            self.escola_turno,
            self.escola_ano_grad,
            self.computador,
            self.computador_compartilhado,
            self.internet,
            self.programa,
            self.trabalha,
            self.empresa_nome,
            self.trabalha_ano_inicio,
            self.trabalha_ano_termino,
            self.outra_graduacao,
            self.outra_graduacao_curso,
            self.outra_graduacao_ano_inicio,
            self.outra_graduacao_ano_fim,
            self.sexo,
            self.ano_nascimento,
            self.estado_civil,
            self.filhos
        ]

    @staticmethod
    def get_lista_atributos():
        return list(Usuario(None, None, None, None).__dict__)[:-1]


class Tentativa(Entidade):

    def __init__(self, periodo, turma, estudante, atividade, questao, seq, tipo, datahora):
        self.datahora = datahora
        self.periodo = periodo
        self.turma = turma
        self.estudante = estudante
        self.atividade = atividade
        self.questao = questao
        self.seq_attempt = seq
        self.tipo = tipo
        #self.code = code
        self.has_err = False
        self.err_msg = None
        self.err_type = None
        self.exec_time = None
        self.tcases_results = None
        self.n_tcases = None
        self.grade = None

    def as_list(self):
        return [
            self.datahora,
            self.periodo,
            self.turma,
            self.estudante,
            self.atividade,
            self.questao,
            self.seq_attempt,
            self.tipo,
            self.has_err,
            self.err_msg,
            self.err_type,
            self.exec_time,
            self.tcases_results,
            self.n_tcases,
            self.grade
        ]

    @staticmethod
    def get_lista_atributos():
        return list(Tentativa(None, None, None, None, None, None, None, None).__dict__)


class Acesso(Entidade):

    def __init__(self, periodo, turma, data, hora, cod_usuario, evento):
        self.periodo = periodo
        self.turma = turma
        self.data = data
        self.hora = hora
        self.codigo_usuario = cod_usuario
        self.evento = evento

    def as_list(self):
        return [
            self.periodo,
            self.turma,
            self.data,
            self.hora,
            self.codigo_usuario,
            self.evento,
        ]

    @staticmethod
    def get_lista_atributos():
        return list(Acesso(None, None, None, None, None, None).__dict__)


class CodeMirror(Entidade):

    def __init__(self, timestamp, data, hora, evento, msg):
        self.timestamp = timestamp
        self.data = data
        self.hora = hora
        self.evento = evento
        self.msg = msg

    def as_list(self):
        return [
            self.timestamp,
            self.data,
            self.hora,
            self.evento,
            self.msg
        ]

    @staticmethod
    def get_lista_atributos():
        return list(CodeMirror(None, None, None, None, None).__dict__)


class Nota(Entidade):

    def __init__(self, periodo, turma, estudante, atividade, nota, correto, incorreto, branco):
        self.periodo = periodo
        self.turma = turma
        self.estudante = estudante
        self.atividade = atividade
        self.nota = nota
        self.correto = correto
        self.incorreto = incorreto
        self.branco = branco

    def as_list(self):
        return [
            self.periodo,
            self.turma,
            self.estudante,
            self.atividade,
            self.nota,
            self.correto,
            self.incorreto,
            self.branco
        ]

    @staticmethod
    def get_lista_atributos():
        return list(Nota(None, None, None, None, None, None, None, None).__dict__)


class SolucaoEstudante(Entidade):

    def __init__(self, periodo, turma, estudante, atividade, exercicio):
        self.periodo = periodo
        self.turma = turma
        self.estudante = estudante
        self.atividade = atividade
        self.exercicio = exercicio
        self.complexity = None
        self.n_classes = None
        self.n_functions = None
        self.loc = None
        self.lloc = None
        self.sloc = None
        self.comments = None
        self.single_comments = None
        self.multi_comments = None
        self.blank_lines = None
        self.h1 = None
        self.h2 = None
        self.N1 = None
        self.N2 = None
        self.h = None
        self.N = None
        self.calculated_N = None
        self.volume = None
        self.difficulty = None
        self.effort = None
        self.bugs = None
        self.time = None
        self.endmarker = None
        self.name = None
        self.number = None
        self.string = None
        self.newline = None
        self.indent = None
        self.dedent = None
        self.lpar = None
        self.rpar = None
        self.lsqb = None
        self.rsqb = None
        self.colon = None
        self.comma = None
        self.semi = None
        self.plus = None
        self.minus = None
        self.star = None
        self.slash = None
        self.vbar = None
        self.amper = None
        self.less = None
        self.greater = None
        self.equal = None
        self.dot = None
        self.percent = None
        self.lbrace = None
        self.rbrace = None
        self.eq_equal = None
        self.not_eq = None
        self.less_eq = None
        self.greater_eq = None
        self.tilde = None
        self.circumflex = None
        self.lshift = None
        self.rshift = None
        self.dbl_star = None
        self.plus_eq = None
        self.minus_eq = None
        self.star_eq = None
        self.slash_eq = None
        self.percent_eq = None
        self.amper_eq = None
        self.vbar_eq = None
        self.circumflex_eq = None
        self.lshift_eq = None
        self.rshift_eq = None
        self.dbl_star_eq = None
        self.dbl_slash = None
        self.dbl_slash_eq = None
        self.at = None
        self.at_eq = None
        self.rarrow = None
        self.ellipsis = None
        self.colon_eq = None
        self.op = None
        self.error_token = None
        self.comment = None
        self.nl = None
        self.encoding = None
        self.number_int = None
        self.number_float = None
        self.kwd_and = None
        self.kwd_or = None
        self.kwd_not = None
        self.kwd_none = None
        self.kwd_false = None
        self.kwd_true = None
        self.kwd_as = None
        self.kwd_assert = None
        self.kwd_async = None
        self.kwd_await = None
        self.kwd_break = None
        self.kwd_class = None
        self.kwd_continue = None
        self.kwd_def = None
        self.kwd_del = None
        self.kwd_if = None
        self.kwd_elif = None
        self.kwd_else = None
        self.kwd_except = None
        self.kwd_finally = None
        self.kwd_for = None
        self.kwd_while = None
        self.kwd_import = None
        self.kwd_from = None
        self.kwd_global = None
        self.kwd_in = None
        self.kwd_is = None
        self.kwd_lambda = None
        self.kwd_nonlocal = None
        self.kwd_pass = None
        self.kwd_raise = None
        self.kwd_return = None
        self.kwd_try = None
        self.kwd_with = None
        self.kwd_yield = None
        self.keyword = None
        self.identifier = None
        self.builtin_type = None
        self.builtin_func = None
        self.kwd_print = None
        self.kwd_input = None
        self.builtin_type_unique = None
        self.builtin_func_unique = None
        self.identifiers_unique = None
        self.identifiers_max_len = None
        self.identifiers_min_len = None
        self.identifiers_mean_len = None

    def as_list(self):
        return [
            self.periodo,
            self.turma,
            self.estudante,
            self.atividade,
            self.exercicio,
            self.complexity,
            self.n_classes,
            self.n_functions,
            self.loc,
            self.lloc,
            self.sloc,
            self.comments,
            self.single_comments,
            self.multi_comments,
            self.blank_lines,
            self.h1,
            self.h2,
            self.N1,
            self.N2,
            self.h,
            self.N,
            self.calculated_N,
            self.volume,
            self.difficulty,
            self.effort,
            self.bugs,
            self.time,
            self.endmarker,
            self.name,
            self.number,
            self.string,
            self.newline,
            self.indent,
            self.dedent,
            self.lpar,
            self.rpar,
            self.lsqb,
            self.rsqb,
            self.colon,
            self.comma,
            self.semi,
            self.plus,
            self.minus,
            self.star,
            self.slash,
            self.vbar,
            self.amper,
            self.less,
            self.greater,
            self.equal,
            self.dot,
            self.percent,
            self.lbrace,
            self.rbrace,
            self.eq_equal,
            self.not_eq,
            self.less_eq,
            self.greater_eq,
            self.tilde,
            self.circumflex,
            self.lshift,
            self.rshift,
            self.dbl_star,
            self.plus_eq,
            self.minus_eq,
            self.star_eq,
            self.slash_eq,
            self.percent_eq,
            self.amper_eq,
            self.vbar_eq,
            self.circumflex_eq,
            self.lshift_eq,
            self.rshift_eq,
            self.dbl_star_eq,
            self.dbl_slash,
            self.dbl_slash_eq,
            self.at,
            self.at_eq,
            self.rarrow,
            self.ellipsis,
            self.colon_eq,
            self.op,
            self.error_token,
            self.comment,
            self.nl,
            self.encoding,
            self.number_int,
            self.number_float,
            self.kwd_and,
            self.kwd_or,
            self.kwd_not,
            self.kwd_none,
            self.kwd_false,
            self.kwd_true,
            self.kwd_as,
            self.kwd_assert,
            self.kwd_async,
            self.kwd_await,
            self.kwd_break,
            self.kwd_class,
            self.kwd_continue,
            self.kwd_def,
            self.kwd_del,
            self.kwd_if,
            self.kwd_elif,
            self.kwd_else,
            self.kwd_except,
            self.kwd_finally,
            self.kwd_for,
            self.kwd_while,
            self.kwd_import,
            self.kwd_from,
            self.kwd_global,
            self.kwd_in,
            self.kwd_is,
            self.kwd_lambda,
            self.kwd_nonlocal,
            self.kwd_pass,
            self.kwd_raise,
            self.kwd_return,
            self.kwd_try,
            self.kwd_with,
            self.kwd_yield,
            self.keyword,
            self.identifier,
            self.builtin_type,
            self.builtin_func,
            self.kwd_print,
            self.kwd_input,
            self.builtin_type_unique,
            self.builtin_func_unique,
            self.identifiers_unique,
            self.identifiers_max_len,
            self.identifiers_min_len,
            self.identifiers_mean_len
        ]

    @staticmethod
    def get_lista_atributos():
        return list(SolucaoEstudante(None, None, None, None, None).__dict__)


class Mousemove(Entidade):

    def __init__(self, data, atividade, exercicio, x, y, evento):
        self.data = data
        self.atividade = atividade
        self.exercicio = exercicio
        self.x = x
        self.y = y
        self.evento = evento

    def as_list(self):
        return [
            self.data,
            self.atividade,
            self.exercicio,
            self.x,
            self.y,
            self.evento
        ]

    @staticmethod
    def get_lista_atributos():
        return list(Mousemove(None, None, None, None, None, None).__dict__)[:]

"""
class SolucaoEstudante(Entidade):

    def __init__(self, periodo: Periodo, turma: Turma, estudante: Estudante, atividade: Atividade, exercicio_codigo: int):
        self.periodo = periodo
        self.turma = turma
        self.estudante = estudante
        self.atividade = atividade
        self.exercicio = exercicio_codigo
        self.tempo_total = None
        self.tempo_foco = None
        self.n_submissoes = None
        self.n_testes = None
        self.n_erros = None
        self.t_execucao = None
        self.nota_final = None
        self.acertou = None
        self.metricas = Metricas(None)
        self.tokens = CodeTokens(None)

    def as_list(self):
        if not self.metricas:
            self.metricas = Metricas(None)
        if not self.tokens:
            self.tokens = CodeTokens(None)
        return [
            self.periodo.descricao,
            self.turma.codigo,
            self.estudante.codigo,
            self.atividade.codigo,
            self.exercicio,
            self.tempo_total,
            self.tempo_foco,
            self.n_submissoes,
            self.n_testes,
            self.n_erros,
            self.t_execucao,
            self.nota_final,
            self.acertou,
            self.metricas.complexity,
            self.metricas.n_classes,
            self.metricas.n_functions,
            self.metricas.loc,
            self.metricas.lloc,
            self.metricas.sloc,
            self.metricas.single_comments,
            self.metricas.comments,
            self.metricas.multilines,
            self.metricas.blank_lines,
            self.metricas.h1,
            self.metricas.h2,
            self.metricas.N1,
            self.metricas.N2,
            self.metricas.h,
            self.metricas.N,
            self.metricas.calculated_N,
            self.metricas.volume,
            self.metricas.difficulty,
            self.metricas.effort,
            self.metricas.bugs,
            self.metricas.time,
            self.tokens.imports,
            self.tokens.assignments,
            self.tokens.assignments_unique,
            self.tokens.kwds,
            self.tokens.kwds_unique,
            self.tokens.lt_numbers,
            self.tokens.lt_strings,
            self.tokens.lt_booleans,
            self.tokens.lgc_op,
            self.tokens.lgc_op_unique,
            self.tokens.and_op,
            self.tokens.or_op,
            self.tokens.not_op,
            self.tokens.arithmetic_op,
            self.tokens.arithmetic_op_unique,
            self.tokens.add_op,
            self.tokens.minus_op,
            self.tokens.mult_op,
            self.tokens.div_op,
            self.tokens.mod_op,
            self.tokens.power_op,
            self.tokens.div_floor_op,
            self.tokens.cmp_op,
            self.tokens.cmp_op_unique,
            self.tokens.equal_op,
            self.tokens.not_eq_op,
            self.tokens.lt_op,
            self.tokens.gt_op,
            self.tokens.less_op,
            self.tokens.greater_op,
            self.tokens.bitwise_op,
            self.tokens.bitwise_op_unique,
            self.tokens.bitwise_and,
            self.tokens.bitwise_or,
            self.tokens.bitwise_xor,
            self.tokens.bitwise_not,
            self.tokens.lshift_op,
            self.tokens.rshift_op,
            self.tokens.identity_op,
            self.tokens.membership_op,
            self.tokens.conditionals,
            self.tokens.ifs,
            self.tokens.elifs,
            self.tokens.elses,
            self.tokens.loops,
            self.tokens.whiles,
            self.tokens.fors,
            self.tokens.breaks,
            self.tokens.continues,
            self.tokens.builtin_f,
            self.tokens.builtin_f_unique,
            self.tokens.type_f,
            self.tokens.type_f_unique,
            self.tokens.lambdas,
            self.tokens.lpar,
            self.tokens.rpar,
            self.tokens.lsqb,
            self.tokens.rsqb,
            self.tokens.lbrace,
            self.tokens.rbrace,
            self.tokens.commas,
            self.tokens.colons,
            self.tokens.dots,
            self.tokens.prints,
            self.tokens.inputs,
            self.tokens.len,
            self.tokens.uident,
            self.tokens.uident_unique,
            self.tokens.uident_mean,
            self.tokens.uident_per_line,
            self.tokens.uident_chars
        ]

    @staticmethod
    def get_lista_atributos():
        return list(SolucaoEstudante(None, None, None, None, 0).__dict__)[:-2]+list(Metricas(None).__dict__)+list(CodeTokens(None).__dict__)

class Solucao(Entidade):

    def as_list(self):
        return [
            self.codigo,
            self.metricas.complexity,
            self.metricas.n_classes,
            self.metricas.n_functions,
            self.metricas.loc,
            self.metricas.lloc,
            self.metricas.sloc,
            self.metricas.single_comments,
            self.metricas.comments,
            self.metricas.multilines,
            self.metricas.blank_lines,
            self.metricas.h1,
            self.metricas.h2,
            self.metricas.N1,
            self.metricas.N2,
            self.metricas.h,
            self.metricas.N,
            self.metricas.calculated_N,
            self.metricas.volume,
            self.metricas.difficulty,
            self.metricas.effort,
            self.metricas.bugs,
            self.metricas.time,
            self.tokens.imports,
            self.tokens.assignments,
            self.tokens.assignments_unique,
            self.tokens.kwds,
            self.tokens.kwds_unique,
            self.tokens.lt_numbers,
            self.tokens.lt_strings,
            self.tokens.lt_booleans,
            self.tokens.lgc_op,
            self.tokens.lgc_op_unique,
            self.tokens.and_op,
            self.tokens.or_op,
            self.tokens.not_op,
            self.tokens.arithmetic_op,
            self.tokens.arithmetic_op_unique,
            self.tokens.add_op,
            self.tokens.minus_op,
            self.tokens.mult_op,
            self.tokens.div_op,
            self.tokens.mod_op,
            self.tokens.power_op,
            self.tokens.div_floor_op,
            self.tokens.cmp_op,
            self.tokens.cmp_op_unique,
            self.tokens.equal_op,
            self.tokens.not_eq_op,
            self.tokens.lt_op,
            self.tokens.gt_op,
            self.tokens.less_op,
            self.tokens.greater_op,
            self.tokens.bitwise_op,
            self.tokens.bitwise_op_unique,
            self.tokens.bitwise_and,
            self.tokens.bitwise_or,
            self.tokens.bitwise_xor,
            self.tokens.bitwise_not,
            self.tokens.lshift_op,
            self.tokens.rshift_op,
            self.tokens.identity_op,
            self.tokens.membership_op,
            self.tokens.conditionals,
            self.tokens.ifs,
            self.tokens.elifs,
            self.tokens.elses,
            self.tokens.loops,
            self.tokens.whiles,
            self.tokens.fors,
            self.tokens.breaks,
            self.tokens.continues,
            self.tokens.builtin_f,
            self.tokens.builtin_f_unique,
            self.tokens.type_f,
            self.tokens.type_f_unique,
            self.tokens.lambdas,
            self.tokens.lpar,
            self.tokens.rpar,
            self.tokens.lsqb,
            self.tokens.rsqb,
            self.tokens.lbrace,
            self.tokens.rbrace,
            self.tokens.commas,
            self.tokens.colons,
            self.tokens.dots,
            self.tokens.prints,
            self.tokens.inputs,
            self.tokens.len,
            self.tokens.uident,
            self.tokens.uident_unique,
            self.tokens.uident_mean,
            self.tokens.uident_per_line,
            self.tokens.uident_chars
        ]

    def __init__(self, codigo: int):
        self.codigo = codigo
        self.metricas = Metricas(None)
        self.tokens = CodeTokens(None)

    @staticmethod
    def get_lista_atributos():
        return list(Solucao(0).__dict__)[:-2]+list(Metricas(None).__dict__)+list(CodeTokens(None).__dict__)

class Metricas:

    def __init__(self, default_value):
        self.complexity = default_value
        self.n_classes = default_value
        self.n_functions = default_value
        self.loc = default_value
        self.lloc = default_value
        self.sloc = default_value
        self.single_comments = default_value
        self.comments = default_value
        self.multilines = default_value
        self.blank_lines = default_value
        self.h1 = default_value
        self.h2 = default_value
        self.N1 = default_value
        self.N2 = default_value
        self.h = default_value
        self.N = default_value
        self.calculated_N = default_value
        self.volume = default_value
        self.difficulty = default_value
        self.effort = default_value
        self.bugs = default_value
        self.time = default_value


class CodeTokens:

    def __init__(self, default_value):
        self.imports = default_value
        self.assignments = default_value
        self.assignments_unique = default_value
        self.kwds = default_value
        self.kwds_unique = default_value
        self.lt_numbers = default_value
        self.lt_strings = default_value
        self.lt_booleans = default_value
        self.lgc_op = default_value
        self.lgc_op_unique = default_value
        self.and_op = default_value
        self.or_op = default_value
        self.not_op = default_value
        self.arithmetic_op = default_value
        self.arithmetic_op_unique = default_value
        self.add_op = default_value
        self.minus_op = default_value
        self.mult_op = default_value
        self.div_op = default_value
        self.mod_op = default_value
        self.power_op = default_value
        self.div_floor_op = default_value
        self.cmp_op = default_value
        self.cmp_op_unique = default_value
        self.equal_op = default_value
        self.not_eq_op = default_value
        self.lt_op = default_value
        self.gt_op = default_value
        self.less_op = default_value
        self.greater_op = default_value
        self.bitwise_op = default_value
        self.bitwise_op_unique = default_value
        self.bitwise_and = default_value
        self.bitwise_or = default_value
        self.bitwise_xor = default_value
        self.bitwise_not = default_value
        self.lshift_op = default_value
        self.rshift_op = default_value
        self.identity_op = default_value
        self.membership_op = default_value
        self.conditionals = default_value
        self.ifs = default_value
        self.elifs = default_value
        self.elses = default_value
        self.loops = default_value
        self.whiles = default_value
        self.fors = default_value
        self.breaks = default_value
        self.continues = default_value
        self.builtin_f = default_value
        self.builtin_f_unique = default_value
        self.type_f = default_value
        self.type_f_unique = default_value
        self.lambdas = default_value
        self.lpar = default_value
        self.rpar = default_value
        self.lsqb = default_value
        self.rsqb = default_value
        self.lbrace = default_value
        self.rbrace = default_value
        self.commas = default_value
        self.colons = default_value
        self.dots = default_value
        self.prints = default_value
        self.inputs = default_value
        self.len = default_value
        self.uident = default_value
        self.uident_unique = default_value
        self.uident_mean = default_value
        self.uident_per_line = default_value
        self.uident_chars = default_value
"""
