# -*- coding: utf-8 -*-
### Codebench Dataset Extractor by Marcos Lima (marcos.lima@icomp.ufam.edu.br)
### Universidade Federal do Amazonas - UFAM
### Instituto de Computação - IComp

import keyword
import re
import statistics
import token
import tokenize
import token_mapping as tkm
import os
import pandas as pd

from collections import Counter, defaultdict
from datetime import datetime

from radon.metrics import h_visit
from radon.raw import analyze
from radon.visitors import ComplexityVisitor

from util import Logger
from model import *

class CodebenchMiner:
    # diretório dos arquivos de saída '.csv' (datasets)
    CSV_FILE_OUTPUT_DIR = os.path.join(os.getcwd(), 'csv')
    OPTION_SOCIAL_DATA = 0
    OPTION_TENTATIVAS_DATA = 1
    OPTION_METRICAS_DATA = 2
    OPTION_MOUSEMOVE_DATA = 3
    OPTION_CODEMIRROR_DATA = 4
    OPTION_GRADES_DATA = 5

    DEFAULT_FILE_ENCODING = 'utf-8'
    DEFAULT_FILE_OPEN_MODE = 'rb'
    PERIODO_CSV_FILENAME = 'periodos.csv'
    TURMA_CSV_FILENAME = 'turmas.csv'
    ATIVIDADE_CSV_FILENAME = 'atividades.csv'
    USUARIO_CSV_FILENAME = 'estudantes.csv'
    TENTATIVA_CSV_FILENAME = 'tentativas.csv'
    METRICAS_ESTUDANTE_CSV_FILENAME = 'metricas_estudantes.csv'

    DATA_FILE_EXTENSION = '.data'

    USUARIO_DATA_FILENAME = 'user.data'
    USUARIO_LINE_SPLIT_PATTERN = '--'
    USUARIO_KEYVALUE_SPLIT_PATTERN = ':'
    USUARIO_ATTR_CONNECTOR_PATTERN = '_'
    USUARIO_FILE_KEY_NAMES = [
        'course_id',
        'course_name',
        'institution_id',
        'course_name',
        'high_school_name',
        'school_type',
        'shift',
        'graduation_year',
        'has_a_pc_at_home',
        'share_this_pc_with_other_people_at_home',
        'this_pc_has_access_to_internet',
        'previous_experience_of_any_computer_language',
        'worked_or_interned_before_the_degree',
        'company_name',
        'year_started_working',
        'year_stopped_working',
        'started_other_degree_programmes',
        'degree_course',
        'year_started_this_degree',
        'sex',
        'year_of_birth',
        'civil_status',
        'have_kids'
    ]

    CODE_FILE_EXTENSION = '.py'

    CODE_BUILTIN_TYPES_LIST = [
        'bool', 'bytes', 'bytearray', 'complex', 'dict', 'float', 'set', 'int', 'list', 'range', 'object', 'str',
        'memoryview', 'None', 'frozenset'
    ]

    CODE_BUILTIN_FUNCS_LIST = [
        'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile',
        'delattr', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter', 'format', 'getattr', 'globals', 'hasattr',
        'hash', 'hex', 'id', 'input', 'isinstance', 'issubclass', 'iter', 'len', 'locals', 'map', 'max', 'min', 'next',
        'oct', 'open', 'ord', 'pow', 'print', 'property', 'range', 'repr', 'reversed', 'round', 'set', 'setattr',
        'slice',
        'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip'
    ]


    @staticmethod
    def extract(path: str, opcoes: dict, view):
        print(path)
        periodos = []
        turmas = []
        atividades = []
        usuarios = []
        tentativas = []
        solucoes = []

        # TODO trocar 'prints' por 'logs' do sistema
        for periodo_dir in os.scandir(path):
            periodo = Periodo(periodo_dir.path.split(os.path.sep)[-1], 0, 0, 0, 0, 0, 0, 0, 0, periodo_dir.path)
            Logger.info(f'NOVO PERIODO ENCONTRADO: {periodo.path}')
            view.update_extraction_status(f'NOVO PERIODO ENCONTRADO: {periodo.path}')
            
            for turma_dir in os.scandir(periodo.path):
                periodo.n_turmas += 1
                Logger.info(f'NOVA TURMA ENCONTRADA: {turma_dir.path}')    
                view.update_extraction_status(f'NOVA TURMA ENCONTRADA: {turma_dir.path}')
                turma =  CodebenchMiner.__extrair_turma(periodo.descricao, turma_dir.path)
                
                for atividade_log in os.scandir(os.path.join(turma_dir.path, 'assessments')):
                    periodo.n_atividades += 1
                    turma.n_atividades += 1
                    Logger.info(f'NOVO LOG DE ATIVIDADE ENCONTRADO: {atividade_log.path}')
                    view.update_extraction_status(f'NOVO LOG DE ATIVIDADE ENCONTRADO: {atividade_log.path}')
                    atividade = CodebenchMiner.__extrair_atividade(periodo.descricao, turma.codigo, atividade_log.path)
                    atividades.append(atividade.as_list())
                
                for usuario_dir in os.scandir(os.path.join(turma_dir.path, 'users')):
                    periodo.n_estudantes += 1
                    turma.n_estudantes += 1

                    if opcoes.get(CodebenchMiner.OPTION_SOCIAL_DATA, False):
                        Logger.info(f'NOVO DIRETORIO DE USUARIO: {usuario_dir.path}')
                        view.update_extraction_status(f'NOVO DIRETORIO DE USUARIO: {usuario_dir.path}')
                        usuario = CodebenchMiner.__extrair_usuario(periodo.descricao, turma.codigo, usuario_dir.path)
                        usuarios.append(usuario.as_list())
                    
                    if opcoes.get(CodebenchMiner.OPTION_TENTATIVAS_DATA, False):    
                        for tentativas_log in os.scandir(os.path.join(usuario_dir.path, 'executions')):
                            periodo.n_tentativas += 1
                            Logger.info(f'NOVO LOG DE TENTATIVAS DE USUARIO: {tentativas_log.path}')
                            view.update_extraction_status(f'NOVO LOG DE TENTATIVAS DE USUARIO: {tentativas_log.path}')
                            tentativas2 = CodebenchMiner.__extrair_tentativas(periodo.descricao, turma.codigo, usuario_dir.path.split(os.path.sep)[-1], tentativas_log.path)
                            tentativas.extend(tentativas2)

                    if opcoes.get(CodebenchMiner.OPTION_METRICAS_DATA, False):
                        for solution_file in os.scandir(os.path.join(usuario_dir.path, 'codes')):
                            periodo.n_codes += 1
                            Logger.info(f'NOVO CODIGO SOLUCAO ESTUDANTE: {solution_file.path}')
                            view.update_extraction_status(f'NOVO CODIGO SOLUCAO ESTUDANTE: {solution_file.path}')
                            usuario = usuario_dir.path.split(os.pathsep)[-1]
                            solucao = CodebenchMiner.__extrair_metricas_solucao_estudantes(periodo.descricao, turma.codigo, usuario, solution_file.path)
                            solucoes.append(solucao.as_list())

                    if opcoes.get(CodebenchMiner.OPTION_CODEMIRROR_DATA, None):    
                        for mirror in os.scandir(os.path.join(usuario.path, 'codemirror')):
                            periodo.n_cmirrors += 1
                            print('NOVO CODEMIRROR LOG ', mirror.path)
                            # TODO extrair codemirror log
                    
                    if opcoes.get(CodebenchMiner.OPTION_GRADES_DATA, False):
                        for grade in os.scandir(os.path.join(usuario.path, 'grades')):
                            periodo.n_grades += 1
                            print('NOVO GRADE LOG ', grade.path)
                            # TODO extrair grade
                    
                    if opcoes.get(CodebenchMiner.OPTION_MOUSEMOVE_DATA, False):
                        for mousemove in os.scandir(os.path.join(usuario.path, 'mousemove')):
                            periodo.n_mousemoves += 1
                            print('NOVO MOUSEMOVE LOG ', mousemove.path)
                            # TODO extrair mousemove

                turmas.append(turma.as_list())
            periodos.append(periodo.as_list())

        # salva os períodos letivos num arquivo csv
        CodebenchMiner.persist(
            periodos,
            os.path.join(CodebenchMiner.CSV_FILE_OUTPUT_DIR, CodebenchMiner.PERIODO_CSV_FILENAME), 
            Periodo.get_lista_atributos()
        )

        # salva as turmas num arquivo csv
        CodebenchMiner.persist(
            turmas,
            os.path.join(CodebenchMiner.CSV_FILE_OUTPUT_DIR, CodebenchMiner.TURMA_CSV_FILENAME), 
            Turma.get_lista_atributos()
        )

        # salva as atividades num arquivo csv
        CodebenchMiner.persist(
            atividades,
            os.path.join(CodebenchMiner.CSV_FILE_OUTPUT_DIR, CodebenchMiner.ATIVIDADE_CSV_FILENAME), 
            Atividade.get_lista_atributos()
        )

        if opcoes[CodebenchMiner.OPTION_SOCIAL_DATA]:
            # salva as atividades num arquivo csv
            CodebenchMiner.persist(
                usuarios,
                os.path.join(CodebenchMiner.CSV_FILE_OUTPUT_DIR, CodebenchMiner.USUARIO_CSV_FILENAME), 
                Usuario.get_lista_atributos()
            )

        if opcoes[CodebenchMiner.OPTION_TENTATIVAS_DATA]:   
            # salva as atividades num arquivo csv
            CodebenchMiner.persist(
                tentativas,
                os.path.join(CodebenchMiner.CSV_FILE_OUTPUT_DIR, CodebenchMiner.TENTATIVA_CSV_FILENAME), 
                Tentativa.get_lista_atributos()
            )
        
        if opcoes[CodebenchMiner.OPTION_METRICAS_DATA]:   
            # salva as metricas de solucao num arquivo csv
            CodebenchMiner.persist(
                solucoes,
                os.path.join(CodebenchMiner.CSV_FILE_OUTPUT_DIR, CodebenchMiner.METRICAS_ESTUDANTE_CSV_FILENAME),
                SolucaoEstudante.get_lista_atributos()
            )

        view.update_extraction_status(f'EXTRAÇÃO FINALIZADA!')

    @staticmethod
    def __extrair_metricas_solucao_estudantes(periodo: str, turma: str, usuario: str, path: str):
        paths = path.split(os.path.sep)[-1].split('_')
        atividade = paths[0]
        exercicio = paths[-1][:-3]
        solucao = SolucaoEstudante(periodo, turma, usuario, atividade, exercicio)

        with open(path, encoding=CodebenchMiner.DEFAULT_FILE_ENCODING) as f:
            CodebenchMiner.__extrair_metricas_codigo(solucao, ''.join(f.readlines()))

        return solucao


    @staticmethod
    def __extrair_metricas_codigo(solucao, codigo: str):
        try:
            v = ComplexityVisitor.from_code(codigo)
            setattr(solucao, 'complexity', v.complexity)
            setattr(solucao, 'n_classes', len(v.classes))
            setattr(solucao, 'n_functions', len(v.functions))
            setattr(solucao, 'funcs_complexity', v.functions_complexity)
            setattr(solucao, 'classes_complexity', v.functions_complexity)
            setattr(solucao, 'total_complexity', v.total_complexity)
            setattr(solucao, 'n_blocks', len(v.blocks))
        except BaseException as err:
            Logger.error(f'FALHA AO EXTRAIR METRICAS DE COMPLEXIDADE: {err}')

        try:
            a = analyze(codigo)
            setattr(solucao, 'loc', a.loc)
            setattr(solucao, 'lloc', a.lloc)
            setattr(solucao, 'sloc', a.sloc)
            setattr(solucao, 'blank_lines', a.blank)
            setattr(solucao, 'comments', a.comments) 
            setattr(solucao, 'single_comments', a.single_comments)
            setattr(solucao, 'multi_comments', a.multi)
        except BaseException as err:
            Logger.error(f'FALHA AO EXTRAIR MÉTRICAS DE TAMANHO: {err}')

        try:
            h = h_visit(codigo)
            setattr(solucao, 'h1', h.total.h1)
            setattr(solucao, 'h2', h.total.h2)
            setattr(solucao, 'N1', h.total.N1)
            setattr(solucao, 'N2', h.total.N2)
            setattr(solucao, 'h', h.total.vocabulary)
            setattr(solucao, 'N', h.total.length)
            setattr(solucao, 'calculated_N', h.total.calculated_length)
            setattr(solucao, 'volume', h.total.volume)
            setattr(solucao, 'difficulty', h.total.difficulty)
            setattr(solucao, 'effort', h.total.effort)
            setattr(solucao, 'bugs', h.total.bugs)
            setattr(solucao, 'time', h.total.time)
        except BaseException as err:
            Logger.error(f'FALHA AO EXTRAIR MÉTRICAS DE QUALIDADE: {err}')

        try:
            token_count = defaultdict(int)
            unique_identifiers = set()
            unique_strings = set()
            unique_btype = set()
            unique_bfunc = set()
            with open(os.path.join(os.getcwd(), 'temp_code.py'), 'w', encoding=CodebenchMiner.DEFAULT_FILE_ENCODING) as temp_code:
                temp_code.write(codigo)
            with tokenize.open(os.path.join(os.getcwd(), 'temp_code.py')) as f:
                try:
                    tokens = tokenize.generate_tokens(f.readline)
                    for tk in tokens:
                        if tk.exact_type == token.NUMBER:
                            if '.' in tk.string:
                                token_count[tkm.NUMBER_FLOAT] += 1
                            else:
                                token_count[tkm.NUMBER_INT] += 1
                        elif tk.type == token.NAME:
                            if keyword.iskeyword(tk.string):
                                token_count[tkm.tk_codes.get(tk.string.lower(), tkm.KEYWORD)] += 1
                            elif tk.string in CodebenchMiner.CODE_BUILTIN_TYPES_LIST:
                                token_count[tkm.BUILTIN_TYPE] += 1
                                unique_btype.add(tk.string)
                            elif tk.string in CodebenchMiner.CODE_BUILTIN_FUNCS_LIST:
                                if tk.string == 'print':
                                    token_count[tkm.KWD_PRINT] += 1
                                elif tk.string == 'input':
                                    token_count[tkm.KWD_INPUT] += 1
                                else:
                                    token_count[tkm.BUILTIN_FUNC] += 1
                                unique_bfunc.add(tk.string)
                            else:
                                token_count[tkm.IDENTIFIER] += 1
                                unique_identifiers.add(tk.string)
                        elif tk.type == token.STRING:
                            token_count[tkm.STRING] += 1
                            unique_strings.add(tk.string)
                        else:
                            token_count[tk.exact_type] += 1
                except BaseException as err:
                    pass

            for k, v in Counter(token_count).items():
                setattr(solucao, tkm.tk_names[k], v)

            setattr(solucao, 'builtin_type_unique', len(unique_btype) if unique_btype else 0)
            setattr(solucao, 'builtin_func_unique', len(unique_bfunc) if unique_bfunc else 0)
            setattr(solucao, 'identifiers_unique', len(unique_identifiers) if unique_identifiers else 0)
            setattr(solucao, 'identifiers_max_len', max([len(x) for x in unique_identifiers]) if unique_identifiers else 0)
            setattr(solucao, 'identifiers_min_len', min([len(x) for x in unique_identifiers]) if unique_identifiers else 0)
            setattr(solucao, 'identifiers_mean_len', statistics.mean([len(x) for x in unique_identifiers]) if unique_identifiers else 0)

        except BaseException as err:
            Logger.error(f'FALHA AO EXTRAIR MÉTRICAS DE TOKENS: {err}')


    @staticmethod
    def __extrair_tentativas(periodo: str, turma: str, usuario: str, path: str):
        seq_attempt = 0
        err_pattern = re.compile('[a-zA-Z]*Error')
        tentativas = []
        nodes = path.split(os.path.sep)
        atividade = nodes[-1].split('_')[0]
        questao = nodes[-1].split('_')[1][:-4]
        with open(path, 'r', encoding=CodebenchMiner.DEFAULT_FILE_ENCODING) as arquivo:
            lines = ''.join(arquivo.readlines())
            for section in lines.split('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*'):
                section = section.strip()
                if section:
                    header, *sub_sections = section.split('\n-- ')
                    tipo, datahora = header.split(' (')
                    tipo = tipo[3:].strip()
                    datahora = datahora.strip()[:-1]
                    code_section, *sub_sections = sub_sections
                    # TODO if sucessful attempt, extract code metrics
                    codigo_estudante = code_section[5:].strip()
                    tentativa = Tentativa(periodo, turma, usuario, atividade, questao, seq_attempt, tipo, datahora)
                    tentativa.tcases_results = []
                    tentativa.n_tcases = 0
                    for sub_section in sub_sections:
                        if sub_section.startswith('EXE'): #EXECUTION TIME
                            tentativa.exec_time = sub_section.split(':\n')[1]
                        elif sub_section.startswith('TES'): #TEST CAS
                            test_seq = sub_section.split('\n---- ')
                            corr_output = test_seq[2].split(':\n')[-1]
                            usr_output = test_seq[3].split(':\n')[-1]
                            if corr_output == usr_output:
                                tentativa.tcases_results.append(True)
                            else:
                                tentativa.tcases_results.append(False)
                            tentativa.n_tcases += 1
                        elif sub_section.startswith('GRA'): #GRADE
                            tentativa.grade = sub_section.split(':')[1].strip()
                        elif sub_section.startswith('ERROR:'):
                            tentativa.has_err = True
                            tentativa.err_msg = sub_section[7:]
                            err_types = err_pattern.findall(tentativa.err_msg)
                            if len(err_types) > 0:
                                tentativa.err_type = err_types[0]
                            else:
                                tentativa.err_type = 'Exception'
                    if not tentativa.has_err:
                        CodebenchMiner.__extrair_metricas_codigo(tentativa, codigo_estudante)
                    tentativas.append(tentativa.as_list())
                    seq_attempt += 1
        return tentativas

    @staticmethod
    def __extrair_turma(periodo: str, path: str):
        turma = Turma(periodo, path.split(os.path.sep)[-1], None, 0, 0, path)
        for entry in os.scandir(os.path.join(path, 'assessments')):
            # se a 'entrada' for um arquivo de extensão '.data' então corresponde atividade
            if entry.is_file() and entry.path.endswith(CodebenchMiner.DATA_FILE_EXTENSION):
                with open(entry.path, CodebenchMiner.DEFAULT_FILE_OPEN_MODE) as f:
                    line = f.readline().decode(CodebenchMiner.DEFAULT_FILE_ENCODING)
                    while line:
                        # ---- class name: Introdução à Programação de Computadores
                        if line.startswith('---- class name:'):
                            turma.descricao = line.strip()[17:]
                            break
                        line = f.readline().decode(CodebenchMiner.DEFAULT_FILE_ENCODING)
        return turma

    @staticmethod
    def __extrair_atividade(periodo: str, turma: str, path: str):
        atividade = Atividade(periodo, turma, path.split(os.path.sep)[-1].replace(CodebenchMiner.DATA_FILE_EXTENSION, ''), path)
        
        with open(path, CodebenchMiner.DEFAULT_FILE_OPEN_MODE) as f:
            Logger.info(f'EXTRAINDO INFORMACOES DE ATIVIDADE DO ARQUIVO: {path}')
            lines = f.readlines()
            atividade.titulo = lines[1].decode(CodebenchMiner.DEFAULT_FILE_ENCODING)[23:].strip()
            atividade.data_inicio = lines[4].decode(CodebenchMiner.DEFAULT_FILE_ENCODING)[12:].strip()
            atividade.data_termino = lines[5].decode(CodebenchMiner.DEFAULT_FILE_ENCODING)[10:].strip()
            atividade.linguagem = lines[6].decode(CodebenchMiner.DEFAULT_FILE_ENCODING)[15:].strip()
            atividade.tipo = lines[8].decode(CodebenchMiner.DEFAULT_FILE_ENCODING)[11:].strip()
            atividade.peso = float(lines[9].decode(CodebenchMiner.DEFAULT_FILE_ENCODING)[13:].strip())
            atividade.n_blocos = int(lines[10].decode(CodebenchMiner.DEFAULT_FILE_ENCODING)[22:].strip())

            atividade.blocos = []
            for line in lines[12:]:
                line = line.decode(CodebenchMiner.DEFAULT_FILE_ENCODING).strip()[18:]
                if line:
                    atividade.blocos.append([int(x) for x in line.split(' or ')])

        return atividade

    @staticmethod
    def __extrair_usuario(periodo: str, turma: str, path: str):
        usuario = Usuario(periodo, turma, path.split(os.path.sep)[-1], path)
        
        dict_obj = {}
        with open(os.path.join(path, CodebenchMiner.USUARIO_DATA_FILENAME), CodebenchMiner.DEFAULT_FILE_OPEN_MODE) as f:
            Logger.info(f'EXTRAINDO INFORMACOES DO USUARIO NO ARQUIVO: {path}')

            data = []
            for line in f.readlines():
                data.append(line.decode(CodebenchMiner.DEFAULT_FILE_ENCODING))
            data = ''.join(data)

            for line in data.split(CodebenchMiner.USUARIO_LINE_SPLIT_PATTERN):
                line = line.strip()
                if line:
                    line = line.split(CodebenchMiner.USUARIO_KEYVALUE_SPLIT_PATTERN)
                    key = line.pop(0)
                    value = ''.join(line)
                    if value:
                        dict_obj[key.lower().replace(' ', CodebenchMiner.USUARIO_ATTR_CONNECTOR_PATTERN)] = value.strip()

        for key, attr in zip(CodebenchMiner.USUARIO_FILE_KEY_NAMES, Usuario.get_lista_atributos()[3:]):
            setattr(usuario, attr, dict_obj.get(key, None))

        return usuario


    @staticmethod
    def persist(entities, path=None, header=None):
        Logger.info(f'Salvando entidades no arquivo de saída: {path}')
        df = pd.DataFrame(entities, columns=header)
        # quoting 2 = NON_NUMERIC (csv.QUOTE_NON_NUMERIC)
        df.to_csv(path, sep=',', index=False, encoding='utf-8', quoting=2)

    @staticmethod
    def create_output_dir():
        """Cria a pasta e os arquivos de saídas '.csv' (datasets)."""
        try:
            # se o diretório de saída existir, apaga seu conteúdo
            if not os.path.exists(CodebenchMiner.CSV_FILE_OUTPUT_DIR):
                os.mkdir(CodebenchMiner.CSV_FILE_OUTPUT_DIR)
        except OSError:
            Logger.error('Erro ao criar diretório de saída dos arquivos CSV!')


class AcessoController(CodebenchMiner):

    __path_users = 'users'
    __file_name = 'logins.log'
    __csv_filename = 'acessos.csv'

    @staticmethod
    def extract(path: str):
        paths = path.split(os.path.sep)
        cod_usuario = paths[-1]
        turma = paths[-3]
        periodo = paths[-4]
        acessos = []
        with open(os.path.join(path, AcessoController.__file_name)) as arquivo:
            for line in arquivo.readlines():
                line = line.split('#')
                acessos.append(Acesso(periodo, turma, line[0][:10], line[0][11:], cod_usuario, line[1][:-2]))
        return acessos

    @staticmethod
    def persist(entities, path=None, header=None):
        return CodebenchMiner.persist(entities, os.path.join(CodebenchMiner.get_output_dir(),
                                                               AcessoController.__csv_filename),
                                        Acesso.get_lista_atributos())


class CodeMirrorController(CodebenchMiner):

    __file_extension = '.log'
    __folder_name = 'codemirror'
    __csv_filename = 'codemirror.csv'
    __pattern = re.compile(r'^\d{4}-\d{1,2}-\d{1,2}')

    @staticmethod
    def extract(path: str):
        codemirror_list = []
        with open(path, 'r', encoding='utf-8') as arquivo:
            for line in [x for x in arquivo.readlines() if CodeMirrorController.__pattern.match(x)]:
                data = line.split('#')
                date_obj = datetime.strptime(data[0].strip(), '%Y-%m-%d %H:%M:%S.%f')
                timestamp = date_obj.timestamp()
                date_split = data[0].strip().split(' ')
                codemirror_ojb = CodeMirror(timestamp, date_split[0], date_split[1], data[1], data[2].strip())
                codemirror_list.append(codemirror_ojb)
        return codemirror_list

    @staticmethod
    def persist(entities, path=None, header=None):
        return CodebenchMiner.persist(entities, os.path.join(CodebenchMiner.get_output_dir(), CodeMirrorController.get_csv_filename()), CodeMirror.get_lista_atributos())

    @staticmethod
    def get_codemirror_file_extension():
        return CodeMirrorController.__file_extension

    @staticmethod
    def get_codemirror_folder_name():
        return CodeMirrorController.__folder_name

    @staticmethod
    def get_csv_filename():
        return CodeMirrorController.__csv_filename


class NotaController(CodebenchMiner):

    __csv_filename = 'notas.csv'
    __folder_name = 'grades'

    @staticmethod
    def extract(path: str):
        paths = path.split(os.path.sep)
        periodo = paths[-6]
        turma = paths[-5]
        estudante = paths[-3]
        atividade = paths[-1][:-4]
        with open(path) as arquivo:
            lines = arquivo.readlines()
            nota = lines[0][19:-1]
            corr = lines[2][14:-1]
            incorr = lines[3][16:-1]
            branco = lines[4][12:]
            return Nota(periodo, turma, estudante, atividade, nota, corr, incorr, branco)

    @staticmethod
    def persist(entities, path=None, header=None):
        return CodebenchMiner.persist(entities,
                                        os.path.join(CodebenchMiner.get_output_dir(), NotaController.get_csv_filename()),
                                        Nota.get_lista_atributos())

    @staticmethod
    def get_grade_folder_name():
        return NotaController.__folder_name

    @staticmethod
    def get_csv_filename():
        return NotaController.__csv_filename


class SolucaoEstudanteController(CodebenchMiner):

    __python_file_extension = '.py'
    __csv_filename = 'metricas_estudantes.csv'
    __folder_name = 'codes'

    __type_list = [
        'bool', 'bytes', 'bytearray', 'complex', 'dict', 'float', 'set', 'int', 'list', 'range', 'object', 'str',
        'memoryview', 'None', 'frozenset'
    ]
    __builtin_types = set(__type_list)

    __f_list = [
        'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile',
        'delattr', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter', 'format', 'getattr', 'globals', 'hasattr',
        'hash', 'hex', 'id', 'input', 'isinstance', 'issubclass', 'iter', 'len', 'locals', 'map', 'max', 'min', 'next',
        'oct', 'open', 'ord', 'pow', 'print', 'property', 'range', 'repr', 'reversed', 'round', 'set', 'setattr',
        'slice',
        'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip'
    ]
    __builtin_funcs = set(__f_list)

    @staticmethod
    def __is_builtin_func(name: str):
        return name in SolucaoEstudanteController.__builtin_funcs

    @staticmethod
    def __is_builtin_type(name: str):
        return name in SolucaoEstudanteController.__builtin_types

    @staticmethod
    def __extract_code_metrics(path: str):
        metricas = dict()
        with open(path) as f:
            codigo = ''.join(f.readlines())

            try:
                v = ComplexityVisitor.from_code(codigo)
                metricas['complexity'] = v.complexity
                metricas['n_functions'] = len(v.functions)
                metricas['n_classes'] = len(v.functions)
            except BaseException as err:
                Logger.error(f'Falha ao extrair métricas de complexidade: {err}')

            try:
                a = analyze(codigo)
                metricas['loc'] = a.loc
                metricas['lloc'] = a.lloc
                metricas['sloc'] = a.sloc
                metricas['blank_lines'] = a.blank
                metricas['comments'] = a.comments
                metricas['single_comments'] = a.single_comments
                metricas['multi_comments'] = a.multi
            except BaseException as err:
                Logger.error(f'Falha ao extrair métricas de tamanho: {err}')

            try:
                h = h_visit(codigo)
                metricas['h1'] = h.total.h1
                metricas['h2'] = h.total.h2
                metricas['N1'] = h.total.N1
                metricas['N2'] = h.total.N2
                metricas['h'] = h.total.vocabulary
                metricas['N'] = h.total.length
                metricas['calculated_N'] = h.total.calculated_length
                metricas['volume'] = h.total.volume
                metricas['difficulty'] = h.total.difficulty
                metricas['effort'] = h.total.effort
                metricas['bugs'] = h.total.bugs
                metricas['time'] = h.total.time
            except BaseException as err:
                Logger.error(f'Falha ao extrair métricas de qualidade: {err}')

            try:
                token_count = defaultdict(int)
                unique_identifiers = set()
                unique_strings = set()
                unique_btype = set()
                unique_bfunc = set()
                with tokenize.open(path) as f:
                    try:
                        tokens = tokenize.generate_tokens(f.readline)
                        for tk in tokens:
                            if tk.exact_type == token.NUMBER:
                                if '.' in tk.string:
                                    token_count[tkm.NUMBER_FLOAT] += 1
                                else:
                                    token_count[tkm.NUMBER_INT] += 1
                            elif tk.type == token.NAME:
                                if keyword.iskeyword(tk.string):
                                    token_count[tkm.tk_codes.get(tk.string.lower(), tkm.KEYWORD)] += 1
                                elif SolucaoEstudanteController.__is_builtin_type(tk.string):
                                    token_count[tkm.BUILTIN_TYPE] += 1
                                    unique_btype.add(tk.string)
                                elif SolucaoEstudanteController.__is_builtin_func(tk.string):
                                    if tk.string == 'print':
                                        token_count[tkm.KWD_PRINT] += 1
                                    elif tk.string == 'input':
                                        token_count[tkm.KWD_INPUT] += 1
                                    else:
                                        token_count[tkm.BUILTIN_FUNC] += 1
                                    unique_bfunc.add(tk.string)
                                else:
                                    token_count[tkm.IDENTIFIER] += 1
                                    unique_identifiers.add(tk.string)
                            elif tk.type == token.STRING:
                                token_count[tkm.STRING] += 1
                                unique_strings.add(tk.string)
                            else:
                                token_count[tk.exact_type] += 1
                    except BaseException as err:
                        pass

                for k, v in Counter(token_count).items():
                    metricas[tkm.tk_names[k]] = v

                metricas['builtin_type_unique'] = len(unique_btype)
                metricas['builtin_func_unique'] = len(unique_bfunc)
                metricas['identifiers_unique'] = len(unique_identifiers)
                metricas['identifiers_max_len'] = max([len(x) for x in unique_identifiers])
                metricas['identifiers_min_len'] = min([len(x) for x in unique_identifiers])
                metricas['identifiers_mean_len'] = statistics.mean([len(x) for x in unique_identifiers])

            except BaseException as err:
                Logger.error(f'Falha ao extrair métricas por tokens: {err}')

        return metricas

    @staticmethod
    def extract(path: str):
        paths = path.split(os.path.sep)
        atividade = paths[-1].split('_')[0]
        exercicio = paths[-1].split('_')[-1][:-3]
        estudante = paths[-3]
        turma = paths[-5]
        periodo = paths[-6]
        solucao = SolucaoEstudante(periodo, turma, estudante, atividade, exercicio)

        metricas = SolucaoEstudanteController.__extract_code_metrics(path)
        for attr, value in metricas.items():
            setattr(solucao, attr, value)

        return solucao

    @staticmethod
    def persist(entities, path=None, header=None):
        return CodebenchMiner.persist(entities, os.path.join(CodebenchMiner.get_output_dir(),
                                                               SolucaoEstudanteController.__csv_filename),
                                        SolucaoEstudante.get_lista_atributos())

    @staticmethod
    def get_codes_folder_name():
        return SolucaoEstudanteController.__folder_name


class MousemoveController(CodebenchMiner):

    __csv_filename = 'mousemoves.csv'
    __folder_name = 'mousemove'

    @staticmethod
    def extract(path: str):
        atividade = path.split(os.path.sep)[-1].replace('.log', '')
        max_x = 3600
        max_y = 1800
        mms = []
        with open(path, 'r') as arq:
            logs = ''.join(arq.readlines())
            logs = logs.replace('\n', '')
            logs = logs.split('},{')
            for log in logs:
                data = log.split(',')
                m = Mousemove(None, atividade, None, None, None, None)
                for value in data:
                    if '"date":' in value:
                        m.data = value.split('":"')[-1][:-1]
                    elif '"e":' in value:
                        if len(data) > 2:
                            m.exercicio = value.split('":')[-1]
                        else :
                            m.evento = value.split('":')[-1]
                    elif '"x":' in value:
                        m.x = value.split('":')[-1]
                        if int(m.x) > max_x:
                            max_x = int(m.x)
                    elif '"y":' in value:
                        m.y = value.split('":')[-1].replace('}','')
                        if int(m.y) > max_y:
                            max_y = int(m.y)
                #print(m.atividade, m.data, m.exercicio, m.x, m.y, m.evento)
                mms.append(m)
        return mms

    @staticmethod
    def persist(entities, path=None, header=None):
        return CodebenchMiner.persist(entities, os.path.join(CodebenchMiner.get_output_dir(),
                                                               MousemoveController.get_csv_filename()),
                                        Mousemove.get_lista_atributos())

    @staticmethod
    def get_csv_filename():
        return MousemoveController.__csv_filename

    @staticmethod
    def get_mousemove_folder_name():
        return MousemoveController.__folder_name


"""
class SolucaoEstudanteController(EntityController):

    ENDMARKER = 0
    NAME = 1
    NUMBER = 2
    STRING = 3
    NEWLINE = 4
    INDENT = 5
    DEDENT = 6
    LPAR = 7
    RPAR = 8
    LSQB = 9
    RSQB = 10
    COLON = 11
    COMMA = 12
    SEMI = 13
    PLUS = 14
    MINUS = 15
    STAR = 16
    SLASH = 17
    VBAR = 18
    AMPER = 19
    LESS = 20
    GREATER = 21
    EQUAL = 22
    DOT = 23
    PERCENT = 24
    LBRACE = 25
    RBRACE = 26
    EQ_EQUAL = 27
    NOT_EQ = 28
    LESS_EQ = 29
    GREATER_EQ = 30
    TILDE = 31
    CIRCUMFLEX = 32
    LSHIFT = 33
    RSHIFT = 34
    DBL_STAR = 35
    PLUS_EQ = 36
    MINUS_EQ = 37
    STAR_EQ = 38
    SLASH_EQ = 39
    PERCENT_EQ = 40
    AMPER_EQ = 41
    VBAR_EQ = 42
    CIRCUMFLEX_EQ = 43
    LSHIFT_EQ = 44
    RSHIFT_EQ = 45
    DBL_STAR_EQ = 46
    DBL_SLASH = 47
    DBL_SLASH_EQ = 48
    AT = 49
    AT_EQ = 50
    RARROW = 51
    ELLIPSIS = 52
    COLON_EQ = 53
    OP = 54
    ERROR_TOKEN = 59
    COMMENT = 60
    NL = 61
    ENCODING = 62
    NUMBER_INT = 63
    NUMBER_FLOAT = 64
    KWD_AND = 65
    KWD_OR = 66
    KWD_NOT = 67
    KWD_NONE = 68
    KWD_FALSE = 69
    KWD_TRUE = 70
    KWD_AS = 71
    KWD_ASSERT = 72
    KWD_ASYNC = 73
    KWD_AWAIT = 74
    KWD_BREAK = 75
    KWD_CLASS = 76
    KWD_CONTINUE = 77
    KWD_DEF = 78
    KWD_DEL = 79
    KWD_IF = 80
    KWD_ELIF = 81
    KWD_ELSE = 82
    KWD_EXCEPT = 83
    KWD_FINALLY = 84
    KWD_FOR = 85
    KWD_WHILE = 86
    KWD_IMPORT = 87
    KWD_FROM = 88
    KWD_GLOBAL = 89
    KWD_IN = 90
    KWD_IS = 91
    KWD_LAMBDA = 92
    KWD_NONLOCAL = 93
    KWD_PASS = 94
    KWD_RAISE = 95
    KWD_RETURN = 96
    KWD_TRY = 97
    KWD_WITH = 98
    KWD_YIELD = 99
    KEYWORD = 100
    IDENTIFIER = 101
    BUILTIN_TYPE = 102
    BUILTIN_FUNC = 103
    KWD_PRINT = 104
    KWD_INPUT = 105
    
    tk_names = {value: name.lower() for name, value in globals().items() if isinstance(value, int)}
    tk_codes = {value: key for key, value in tk_names.items()}

    __csv_filename = 'estudantes.csv'
    __estudante_folder_name = 'users'
    __tentativas_folder_name = 'executions'
    __codemirror_file_extension = '.log'
    __codemirror_file_open_mode = 'rU'
    __codemirror_file_encoding = 'utf-8'
    __codemirror_file_datetime_fmt = '%Y-%m-%d %H:%M:%S.%f'
    __atividade_file_datetime_fmt = '%Y-%m-%d %H:%M'
    __python_file_extension = '.py'

    # limite do intervalo de tempo entre eventos de interação com o CodeMirror duranet a implementação de uma Solução
    # qualquer intervalo maior que o limite abaixo é considerado ociosidade
    __limite_ociosidade = timedelta(minutes=5)


    @staticmethod
    def extract(path: str):
        atividades = {a.codigo: a for a in estudante.turma.atividades}
        with os.scandir(os.path.join(estudante.path, TentativaController.__tentativas_folder_name)) as nodes:
            for node in nodes:
                # se a 'entrada' for um arquivo de extensão '.log', então corresponde as execuções de uma questão.
                if node.is_file() and node.path.endswith(TentativaController.__codemirror_file_extension):
                    Logger.info(f'Extraindo informações de Execução: {arquivo.name}')
                    # divide o nome do arquivo obtendo os códigos da atividade e exercício.
                    atividade_code, exercicio_code, *_ = arquivo.name.replace(
                        TentativaController.__codemirror_file_extension, '').split('_')
                    atividade = atividades.get(int(atividade_code), None)
                    execucao = Execucao(estudante.periodo, estudante.turma, estudante, atividade, int(exercicio_code))

                    TentativaController.__extract_executions_count(arquivo.path, execucao)

                    codemirror_file = os.path.join(estudante.path, 'codemirror', arquivo.name)
                    if os.path.exists(codemirror_file):
                        TentativaController.__extract_solution_interval(codemirror_file, execucao)
                    else:
                        Logger.warn(f'Arquivo de execução não encontrado: {codemirror_file}')

                    if not execucao.metricas or not execucao.tokens:
                        code_file = arquivo.name.replace(TentativaController.__codemirror_file_extension,
                                                         TentativaController.__python_file_extension)
                        code_file = os.path.join(estudante.path, 'codes', code_file)
                        if os.path.exists(code_file):
                            try:
                                with open(code_file) as f:
                                    codigo = ''.join(f.readlines())
                                execucao.metricas = TentativaController.__extract_code_metrics(codigo)
                            except Exception as e:
                                execucao.metricas = None
                                Logger.error(f'Erro ao extrair métricas do arquivo, {str(e)}: {code_file}')
                            try:
                                execucao.tokens = TentativaController.__extract_code_tokens(code_file)
                            except Exception as e:
                                execucao.tokens = None
                                Logger.error(f'Erro ao extrair tokens do arquivo, {str(e)}: {code_file}')
                        else:
                            Logger.warn(f'Arquivo de código fonte não encontrado: {code_file}')

                    estudante.execucoes.append(execucao)

    @staticmethod
    def __extract_solution_interval(path: str, execucao: Tentativa):
        with open(path, TentativaController.__codemirror_file_open_mode, encoding=TentativaController.__codemirror_file_encoding) as f:
            Logger.info(f'Calculando tempos des implementação e interação: {path}')
            # datas de inicio e termino da atividade, servem como limites para o calculo do tempo e solução

            atividade_data_inicio = datetime.strptime(execucao.atividade.data_inicio, TentativaController.__atividade_file_datetime_fmt)
            atividade_data_fim = datetime.strptime(execucao.atividade.data_termino, TentativaController.__atividade_file_datetime_fmt)

            # algumas turmas são dividas durante os exames, por isso aumento o intervalo de tempo
            if execucao.atividade.tipo == 'exam':
                atividade_data_inicio -= timedelta(hours=2)
                atividade_data_fim += timedelta(hours=2)

            execucao.tempo_total = timedelta(0)
            execucao.tempo_foco = timedelta(0)

            # percorremos o arquivo de log até os eventos terem um datetime maior que o do inicio da atividade
            line = f.readline()
            at_open = True
            while line and at_open:
                event_datetime, event_name, event_msg = TentativaController.__get_event_info(line)
                if event_name == 'focus' and event_datetime and (event_datetime >= atividade_data_inicio):
                    last_interaction = event_datetime
                    line = f.readline()
                    while line and event_name != 'blur':
                        next_interaction, event_name, event_msg = TentativaController.__get_event_info(line)
                        if next_interaction:
                            if next_interaction > atividade_data_fim:
                                at_open = False
                                break
                            intervalo = next_interaction - last_interaction
                            execucao.tempo_total += intervalo
                            if intervalo <= TentativaController.__limite_ociosidade:
                                execucao.tempo_foco += intervalo
                            last_interaction = next_interaction
                        line = f.readline()
                line = f.readline()


    @staticmethod
    def __get_event_info(log_line: str):
        try:
            date, _, log_line = log_line.partition('#')
            name, _, msg = log_line.partition('#')
            # data e hora do evento desconsiderando os milisegundos
            date = datetime.strptime(date, TentativaController.__codemirror_file_datetime_fmt)
            return date, name, msg
        except Exception:
            #TODO throws exception
            return None, '', ''

    @staticmethod
    def __extract_executions_count(path: str, execucao: Tentativa):
        error_names = []
        with open(path, 'r', encoding='latin-1') as f:
            execucao.n_submissoes = 0
            execucao.n_testes = 0
            execucao.n_erros = 0
            execucao.nota_final = 0.0

            i = 0
            lines = f.readlines()
            size = len(lines)

            while i < size:
                if lines[i].startswith('== S'):
                    execucao.t_execucao = None
                    execucao.acertou = False
                    execucao.n_submissoes += 1
                    i += 1
                    while not lines[i].startswith('*-*'):
                        if lines[i].startswith('-- CODE'):
                            i += 1
                            code_start_line = i
                            while not lines[i].startswith('-- '):
                                i += 1
                            code_end_line = i
                        elif lines[i].startswith('-- EXEC'):
                            value = lines[i + 1].strip()
                            try:
                                execucao.t_execucao = float(value)
                            except Exception:
                                execucao.t_execucao = None
                            i += 2
                        elif lines[i].startswith('-- GRAD'):
                            value = lines[i + 1].strip()[:-1]
                            try:
                                execucao.nota_final = float(value)
                            except Exception:
                                execucao.nota_final = None
                            i += 2
                        elif lines[i].startswith('-- ERROR'):
                            execucao.n_erros += 1
                            i += 2
                            while not lines[i].startswith('*-*'):
                                m = re.match(r"^([\w_\.]+Error)", lines[i])
                                if m:
                                    error_names.append(m.group(0))
                                i += 1
                        else:
                            i += 1

                    if execucao.nota_final > 99.99:
                        code = ''.join(lines[code_start_line:code_end_line])
                        execucao.acertou = True
                        try:
                            execucao.metricas = TentativaController.__extract_code_metrics(code)
                        except Exception as e:
                            execucao.nota_final = 0.0
                            execucao.acertou = False
                            execucao.metricas = None
                            Logger.error(f'Erro ao extrair métricas do log de execucoes, {str(e)}: {path}')
                        try:
                            with open('temp.py', 'w', encoding='latin-1') as temp:
                                temp.write(code)
                            execucao.tokens = TentativaController.__extract_code_tokens('temp.py')
                        except Exception as e:
                            execucao.nota_final = 0.0
                            execucao.acertou = False
                            execucao.tokens = None
                            Logger.error(f'Erro ao extrair tokens do log de execucoes: {str(e)}: {path}')

                        if execucao.acertou:
                            i = size + 1

                elif lines[i].startswith('== T'):
                    execucao.n_testes += 1
                    while not lines[i].startswith('*-*'):
                        if lines[i].startswith('-- ERROR'):
                            execucao.n_erros += 1
                            i += 2
                            while not lines[i].startswith('*-*'):
                                m = re.match(r"^([\w_\.]+Error)", lines[i])
                                if m:
                                    error_names.append(m.group(0))
                                i += 1
                        else:
                            i += 1
                i += 1

        erros_count = Util.count_errors(error_names, execucao)
        if len(erros_count):
            CSVParser.salvar_erros(erros_count)

class SolucaoController:

    # extensão do arquivo de código-fonte das soluções dos 'Professores
    __solution_extension = '.code'

    __module_token = {
        'import': True,
        'from': True
    }

    __type_token = {
        'bool': True,
        'bytes': True,
        'bytearray': True,
        'complex': True,
        'dict': True,
        'float': True,
        'set': True,
        'int': True,
        'list': True,
        'range': True,
        'object': True,
        'str': True,
        'memoryview': True,
        'None': True,
        'frozenset': True
    }

    __builtin_token = {
        'abs': True,
        'all': True,
        'any': True,
        'ascii': True,
        'bin': True,
        'bool': True,
        'breakpoint': True,
        'bytearray': True,
        'bytes': True,
        'callable': True,
        'chr': True,
        'classmethod': True,
        'compile': True,
        'complex': True,
        'delattr': True,
        'dict': True,
        'dir': True,
        'divmod': True,
        'enumerate': True,
        'eval': True,
        'exec': True,
        'filter': True,
        'float': True,
        'format': True,
        'frozenset': True,
        'getattr': True,
        'globals': True,
        'hasattr': True,
        'hash': True,
        'hex': True,
        'id': True,
        'input': True,
        'int': True,
        'isinstance': True,
        'issubclass': True,
        'iter': True,
        'len': True,
        'list': True,
        'locals': True,
        'map': True,
        'max': True,
        'min': True,
        'next': True,
        'object': True,
        'oct': True,
        'open': True,
        'ord': True,
        'pow': True,
        'print': True,
        'property': True,
        'range': True,
        'repr': True,
        'reversed': True,
        'round': True,
        'set': True,
        'setattr': True,
        'slice': True,
        'sorted': True,
        'staticmethod': True,
        'str': True,
        'sum': True,
        'super': True,
        'tuple': True,
        'type': True,
        'vars': True,
        'zip': True,
    }

    @staticmethod
    def __is_import_token(t: tokenize.TokenInfo):
        if t.start[1] == 0:
            return SolucaoController.__module_token.get(t.string, False)
        return False

    @staticmethod
    def extract_solucoes(path: str):
        solucoes = []
        # coleta todas os arquivos/pastas dentro do diretório de execuções do aluno
        with os.scandir(path) as arquivos:
            for arquivo in arquivos:
                # se a 'entrada' for um arquivo de extensão '.code', então corresponde as execuções de uma questão.
                if arquivo.is_file() and arquivo.path.endswith(SolucaoController.__solution_extension):
                    Logger.info(f'Extraindo métricas da Solução: {arquivo.path}')
                    solucao = Solucao(int(arquivo.name.replace(SolucaoController.__solution_extension, '')))
                    with open(arquivo.path, 'rU') as f:
                        codigo = ''.join(f.readlines())
                    try:
                        solucao.metricas = SolucaoController.__extract_code_metrics(codigo)
                        solucao.tokens = SolucaoController.__extract_code_tokens(arquivo.path)
                        solucoes.append(solucao)
                    except Exception as e:
                        Logger.error(f'Não foi possível extrair métricas e tokens do códigodo instrutor: {arquivo.path}')

        return solucoes

    @staticmethod
    def __extract_code_tokens(path: str):
        # TODO relatório das builtin functions mais recorrentes
        # TODO relatório das type functions mais recorrentes
        # TODO relatório dos operadores mais recorrentes
        ct = CodeTokens(0)
        kwd_unique = set()  # unique keywords
        lgc_unique = set()  # unique logical operators
        btf_unique = set()  # unique bultin_functions
        tpf_unique = set()  # unique type_functions
        asg_unique = set()  # unique assignment operators
        art_unique = set()  # unique arithmeti operators
        cmp_unique = set()  # unique comparison operators
        btw_unique = set()  # unique bitwise operators
        id_per_line = []  # identifiers per line
        id_unique = set()  # unique user identifiers
        line = 0

        with tokenize.open(path) as f:
            tokens = tokenize.generate_tokens(f.readline)
            for token in tokens:
                exact_type = token.exact_type
                if keyword.iskeyword(token.string):
                    ct.kwds += 1
                    kwd_unique.add(token.string)
                    if token.string == 'if':
                        ct.conditionals += 1
                        ct.ifs += 1
                    elif token.string == 'else':
                        ct.conditionals += 1
                        ct.elses += 1
                    elif token.string == 'elif':
                        ct.conditionals += 1
                        ct.elifs += 1
                    elif token.string == 'while':
                        ct.loops += 1
                        ct.whiles += 1
                    elif token.string == 'for':
                        ct.loops += 1
                        ct.fors += 1
                    elif token.string == 'and':
                        ct.lgc_op += 1
                        ct.and_op += 1
                        lgc_unique.add(token.string)
                    elif token.string == 'or':
                        ct.lgc_op += 1
                        ct.or_op += 1
                        lgc_unique.add(token.string)
                    elif token.string == 'not':
                        ct.lgc_op += 1
                        ct.not_op += 1
                        lgc_unique.add(token.string)
                    elif token.string == 'True' or token.string == 'False':
                        ct.lt_booleans += 1
                    elif SolucaoController.__is_import_token(token):
                        ct.imports += 1
                    elif token.string == 'break':
                        ct.breaks += 1
                    elif token.string == 'continue':
                        ct.continues += 1
                    elif token.string == 'is':
                        ct.identity_op += 1
                    elif token.string == 'in':
                        ct.membership_op += 1
                    elif token.string == 'lambda':
                        ct.lambdas += 1
                elif SolucaoController.__builtin_token.get(token.string, False):  # if is a builtin function
                    ct.builtin_f += 1
                    btf_unique.add(token.string)
                    if SolucaoController.__type_token.get(token.string, False):
                        ct.type_f += 1
                        tpf_unique.add(token.string)
                    elif token.string == 'print':
                        ct.prints += 1
                    elif token.string == 'input':
                        ct.inputs += 1
                    elif token.string == 'len':
                        ct.len += 1
                elif token.type == tokenize.OP:
                    # operador de atribuição ou atribuição composta
                    if exact_type == tokenize.EQUAL or (tokenize.PLUSEQUAL <= exact_type <= tokenize.DOUBLESTAREQUAL) or exact_type == tokenize.DOUBLESLASHEQUAL:
                        ct.assignments += 1
                        asg_unique.add(token.string)
                        if exact_type == tokenize.PLUSEQUAL:  # operador '+='
                            ct.arithmetic_op += 1
                            art_unique.add('+')
                            ct.add_op += 1
                        elif exact_type == tokenize.MINEQUAL:  # operador '-='
                            ct.arithmetic_op += 1
                            art_unique.add('-')
                            ct.minus_op += 1
                        elif exact_type == tokenize.STAREQUAL:  # operador '*='
                            ct.arithmetic_op += 1
                            art_unique.add('*')
                            ct.mult_op += 1
                        elif exact_type == tokenize.SLASHEQUAL:  # operador '/='
                            ct.arithmetic_op += 1
                            art_unique.add('/')
                            ct.div_op += 1
                        elif exact_type == tokenize.PERCENTEQUAL:  # operador '%='
                            ct.arithmetic_op += 1
                            art_unique.add('%')
                            ct.mod_op += 1
                        elif exact_type == tokenize.DOUBLESLASHEQUAL:  # operador '//='
                            ct.arithmetic_op += 1
                            art_unique.add('//')
                            ct.div_floor_op += 1
                        elif exact_type == tokenize.DOUBLESTAREQUAL:  # operador '**='
                            ct.arithmetic_op += 1
                            art_unique.add('**')
                            ct.power_op += 1
                        elif exact_type == tokenize.AMPEREQUAL:  # operador '&='
                            ct.bitwise_op += 1
                            btw_unique.add('&')
                            ct.bitwise_and += 1
                        elif exact_type == tokenize.VBAREQUAL:  # operador '|='
                            ct.bitwise_op += 1
                            btw_unique.add('|')
                            ct.bitwise_or += 1
                        elif exact_type == tokenize.CIRCUMFLEXEQUAL:  # operador '^='
                            ct.bitwise_op += 1
                            btw_unique.add('^')
                            ct.bitwise_xor += 1
                        elif exact_type == tokenize.LEFTSHIFTEQUAL:  # operador '<<='
                            ct.bitwise_op += 1
                            btw_unique.add('<<')
                            ct.lshift_op += 1
                        elif exact_type == tokenize.RIGHTSHIFTEQUAL:  # operador '>>='
                            ct.bitwise_op += 1
                            btw_unique.add('>>')
                            ct.rshift_op += 1
                    # operador aritmético
                    elif tokenize.PLUS <= exact_type <= tokenize.SLASH or exact_type == tokenize.PERCENT or exact_type == tokenize.DOUBLESTAR or exact_type == tokenize.DOUBLESLASH:
                        ct.arithmetic_op += 1
                        art_unique.add(token.string)
                        if exact_type == tokenize.PLUS:  # operador '+'
                            ct.add_op += 1
                        elif exact_type == tokenize.MINUS:  # operador '-'
                            ct.minus_op += 1
                        elif exact_type == tokenize.STAR:  # operador '*'
                            ct.mult_op += 1
                        elif exact_type == tokenize.SLASH:  # operador '/'
                            ct.div_op += 1
                        elif exact_type == tokenize.PERCENT:  # operador '%'
                            ct.mod_op += 1
                        elif exact_type == tokenize.DOUBLESTAR:  # operador '**'
                            ct.power_op += 1
                        elif exact_type == tokenize.DOUBLESLASH:  # operador '//'
                            ct.div_floor_op += 1
                    # operador de comparação I
                    elif tokenize.EQEQUAL <= exact_type <= tokenize.GREATEREQUAL:
                        ct.cmp_op += 1
                        cmp_unique.add(token.string)
                        if tokenize.EQEQUAL:  # operador '=='
                            ct.equal_op += 1
                        elif tokenize.NOTEQUAL:  # operador '!='
                            ct.not_eq_op += 1
                        elif exact_type == tokenize.LESSEQUAL:  # operador '<='
                            ct.lt_op += 1
                        elif exact_type == tokenize.GREATEREQUAL:  # operador '>='
                            ct.gt_op += 1
                    # operador de comparação II
                    elif exact_type == tokenize.LESS:  # operador '<'
                        ct.cmp_op += 1
                        cmp_unique.add(token.string)
                        ct.less_op += 1
                    # operador de comparação III
                    elif exact_type == tokenize.GREATER:  # operador '>'
                        ct.cmp_op += 1
                        cmp_unique.add(token.string)
                        ct.greater_op += 1
                    # operadores bitwise
                    elif exact_type == tokenize.VBAR or exact_type == tokenize.AMPER or (tokenize.TILDE <= exact_type <= tokenize.RIGHTSHIFT):
                        ct.bitwise_op += 1
                        btw_unique.add(token.string)
                        if exact_type == tokenize.AMPER:  # operador '&'
                            ct.bitwise_and += 1
                        elif exact_type == tokenize.VBAR:  # operador '|'
                            ct.bitwise_or += 1
                        elif exact_type == tokenize.TILDE:  # operador '~'
                            ct.bitwise_not += 1
                        elif exact_type == tokenize.CIRCUMFLEX:  # operador '^'
                            ct.bitwise_xor += 1
                        elif exact_type == tokenize.RIGHTSHIFT:  # operador '>>'
                            ct.rshift_op += 1
                        elif exact_type == tokenize.LEFTSHIFT:  # operador '<<'
                            ct.lshift_op += 1
                    elif exact_type == tokenize.LPAR:  # operador '('
                        ct.lpar += 1
                    elif exact_type == tokenize.RPAR:  # operador ')'
                        ct.rpar += 1
                    elif exact_type == tokenize.LSQB:  # operador '['
                        ct.lsqb += 1
                    elif exact_type == tokenize.RSQB:  # operador ']'
                        ct.rsqb += 1
                    elif exact_type == tokenize.LBRACE:  # operador '{'
                        ct.lbrace += 1
                    elif exact_type == tokenize.RBRACE:  # operador '}'
                        ct.rbrace += 1
                    elif exact_type == tokenize.COMMA:  # operador ','
                        ct.commas += 1
                    elif exact_type == tokenize.COLON:  # operador ':'
                        ct.colons += 1
                    elif exact_type == tokenize.DOT:  # operador '.'
                        ct.dots += 1
                elif token.type == tokenize.NUMBER:
                    ct.lt_numbers += 1
                elif token.type == tokenize.STRING:
                    ct.lt_strings += 1
                elif token.type == tokenize.NAME:
                    id_unique.add(token.string)
                    if token.start[0] == line:
                        id_per_line[-1] += 1
                    else:
                        id_per_line.append(1)
                        line = token.start[0]

        ct.kwds_unique = len(kwd_unique)
        ct.lgc_op_unique = len(lgc_unique)
        ct.builtin_f_unique = len(btf_unique)
        ct.type_f_unique = len(tpf_unique)
        ct.assignments_unique = len(asg_unique)
        ct.arithmetic_op_unique = len(art_unique)
        ct.cmp_op_unique = len(cmp_unique)
        ct.bitwise_op_unique = len(btw_unique)
        ct.uident = sum(id_per_line)
        ct.uident_unique = len(id_unique)
        if len(id_per_line) > 0:
            ct.uident_mean = mean(id_per_line)
        else:
            ct.uident_mean = 0.0
        if token.end[0] > 0:
            ct.uident_per_line = ct.uident / token.end[0]
        else:
            ct.uidentifiers_per_lin = 0.0

        if ct.uident_unique > 0:
            char_total = 0
            for identifier in id_unique:
                char_total += len(identifier)
            ct.uident_chars = char_total / ct.uident_unique
        else:
            ct.uident_chars = 0.0

        return ct
"""
