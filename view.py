# -*- coding: utf-8 -*-
### Codebench Dataset Extractor by Marcos Lima (marcos.lima@icomp.ufam.edu.br)
### Universidade Federal do Amazonas - UFAM
### Instituto de Computação - IComp
import os
import tkinter as tk

from controller import PeriodoController, TurmaController, AtividadeController, UsuarioController, \
    TentativaController, AcessoController, NotaController, MousemoveController, CodeMirrorController, SolucaoEstudanteController
from util import Logger


class MainScreen:

    __dataset_path = ''

    def __init__(self, name, version):
        self.name = name
        self.version = version

        self.root = tk.Tk()
        self.root.title(string=f'{name} v{version}')

        self.frm_codebench = tk.Frame(master=self.root, relief=tk.GROOVE, borderwidth=5, padx=5, pady=5)
        self.frm_codebench.pack(side=tk.TOP)

        self.dataset_path = tk.StringVar(self.root)

        self.lbl_codebench_path = tk.Label(master=self.frm_codebench, text='INSIRA O CAMINHO PARA O DATASET CODEBENCH: ', anchor='w')
        self.lbl_codebench_path.pack(fill=tk.X, side=tk.TOP)
        self.ent_codebench_path = tk.Entry(master=self.frm_codebench, width=120, textvariable=self.dataset_path)
        self.ent_codebench_path.pack(fill=tk.X, side=tk.BOTTOM)

        self.frm_buttons = tk.Frame(master=self.root, relief=tk.FLAT, borderwidth=5, padx=5, pady=5)
        self.frm_buttons.pack(side=tk.BOTTOM, fill=tk.X)

        self.progress_string = tk.StringVar()
        self.progress_string.set('Progresso...')
        self.progress_lb = tk.Label(self.frm_buttons, textvariable=self.progress_string)

        self.btn_sociais = tk.Button(master=self.frm_buttons, text='EXTRAIR DADOS SOCIAIS', command=self.btn_sociais_click)
        self.btn_sociais.pack(fill=tk.X)

        self.btn_tentativas = tk.Button(master=self.frm_buttons, text='EXTRAIR DADOS DAS TENTATIVAS DE SOLUCAO', command=self.btn_tentativas_click)
        self.btn_tentativas.pack(fill=tk.X)

        self.btn_solucoes = tk.Button(master=self.frm_buttons, text='EXTRAIR MÉTRICAS DE CÓDIGOS DOS ESTUDANTES', command=self.btn_solucoes_click)
        self.btn_solucoes.pack(fill=tk.X)

        self.btn_mouve = tk.Button(master=self.frm_buttons, text='EXTRAIR EVENTOS DE MOUSE EM ATIVIDADES', command=self.btn_mouse_click)
        self.btn_mouve.pack(fill=tk.X)

        self.progress_lb.pack(fill=tk.X)

        self.root.mainloop()

    def get_dataset_path(self):
        MainScreen.__dataset_path = self.dataset_path.get()
        return MainScreen.__dataset_path

    def btn_sociais_click(self):
        try:
            p = self.__extract_periodos_from_dataset(self.get_dataset_path())
            PeriodoController.persist(p)

            t = self.__extract_turmas_from_dataset(p)
            TurmaController.persist(t)

            a = self.__extract_atividades_from_dataset(t)
            AtividadeController.persist(a)

            u = self.__extract_usuarios_from_dataset(t)
            UsuarioController.persist(u)

            ac = self.__extract_acessos_from_dataset(u)
            AcessoController.persist(ac)

            self.progress_string.set('CONCLUÍDO!!!')
            self.progress_lb.update_idletasks()

        except BaseException as err:
            Logger.error(f'Erro ao extrair informações: {err}')

    def btn_tentativas_click(self):
        try:
            p = self.__extract_periodos_from_dataset(self.get_dataset_path())
            t = self.__extract_turmas_from_dataset(p)
            usuarios = self.__extract_usuarios_from_dataset(t)

            tentativas = []
            codemirror = []
            notas = []
            for usuario in usuarios:
                with os.scandir(os.path.join(usuario.path, TentativaController.get_execucoes_folder_name())) as nodes_ex:
                    for node_ex in nodes_ex:
                        if node_ex.is_file():
                            Logger.info(f'Extraindo tentativas do arquivo: {node_ex.path}')
                            tentativas.extend(TentativaController.extract(node_ex.path))
                with os.scandir(os.path.join(usuario.path, CodeMirrorController.get_codemirror_folder_name())) as nodes_m:
                    for node_m in nodes_m:
                        if node_m.is_file():
                            Logger.info(f'Extraindo logs do codemirror do arquivo: {node_ex.path}')
                            codemirror.extend(TentativaController.extract(node_m.path))
                with os.scandir(os.path.join(usuario.path, NotaController.get_grade_folder_name())) as nodes_g:
                    for node_g in nodes_g:
                        if node_g.is_file() and not node_g.name.startswith('final_grade'):
                            Logger.info(f'Extraindo notas do arquivo: {node_g.path}')
                            notas.append(NotaController.extract(node_g.path))
            TentativaController.persist(tentativas)
            CodeMirrorController.persist(codemirror)
            NotaController.persist(notas)
            self.progress_string.set('Tarefa Concluída!')
            self.progress_lb.update_idletasks()

        except BaseException as err:
            Logger.error(f'Erro ao extrair informações: {err}')

    def btn_solucoes_click(self):
        try:
            p = self.__extract_periodos_from_dataset(self.get_dataset_path())
            t = self.__extract_turmas_from_dataset(p)
            usuarios = self.__extract_usuarios_from_dataset(t)

            metricas = []
            for usuario in usuarios:
                with os.scandir(os.path.join(usuario.path, SolucaoEstudanteController.get_codes_folder_name())) as nodes_c:
                    for node_c in nodes_c:
                        if node_c.is_file():
                            Logger.info(f'Extraindo métricas de código do arquivo: {node_c.path}')
                            metricas.append(SolucaoEstudanteController.extract(node_c.path))
            SolucaoEstudanteController.persist(metricas)
            self.progress_string.set('Tarefa Concluída!')
            self.progress_lb.update_idletasks()

        except BaseException as err:
            Logger.error(f'Erro ao extrair informações: {err}')

    def btn_mouse_click(self):
        try:
            p = self.__extract_periodos_from_dataset(self.get_dataset_path())
            t = self.__extract_turmas_from_dataset(p)
            usuarios = self.__extract_usuarios_from_dataset(t)

            moves = []
            for usuario in usuarios:
                with os.scandir(os.path.join(usuario.path, MousemoveController.get_mousemove_folder_name())) as nodes_mv:
                    for node_mv in nodes_mv:
                        if node_mv.is_file():
                            Logger.info(f'Extraindo logs de mousemove do arquivo: {node_mv.path}')
                            moves.extend(MousemoveController.extract(node_mv.path))
            MousemoveController.persist(moves)
            self.progress_string.set('Tarefa Concluída!')
            self.progress_lb.update_idletasks()

        except BaseException as err:
            Logger.error(f'Erro ao extrair informações: {err}')

    def __extract_periodos_from_dataset(self, path: str):
        periodos = []
        with os.scandir(path) as nodes_p:
            for node_p in nodes_p:
                if node_p.is_dir():
                    Logger.info(f'Dados de periodo encontrados no caminho: {node_p.path}')
                    # view_string.set(f'Dados de periodo encontrados no caminho: {node_p.path}')
                    # view_progress.update_idletasks()
                    periodos.append(PeriodoController.extract(node_p.path))
        return periodos

    def __extract_turmas_from_dataset(self, periodos):
        turmas = []
        for periodo in periodos:
            with os.scandir(periodo.path) as nodes_t:
                for node_t in nodes_t:
                    if node_t.is_dir():
                        turmas.append(TurmaController.extract(node_t.path))
                        # Logger.info(f'Dados de turma encontrados no caminho: {node_t.path}')
                        # self.progress_string.set(f'Dados de turma encontrados no caminho: {node_t.path}')
                        # self.progress_lb.update_idletasks()
        return turmas

    def __extract_atividades_from_dataset(self, turmas):
        atividades = []
        for turma in turmas:
            with os.scandir(os.path.join(turma.path, AtividadeController.get_atividade_folder_name())) as nodes_a:
                for node_a in nodes_a:
                    if node_a.is_file() and node_a.name.endswith('.data'):
                        atividades.append(AtividadeController.extract(node_a.path))
        return atividades

    def __extract_usuarios_from_dataset(self, turmas):
        usuarios = []
        for turma in turmas:
            with os.scandir(os.path.join(turma.path, UsuarioController.get_usuario_folder_name())) as nodes_u:
                for node_u in nodes_u:
                    if node_u.is_dir():
                        usuarios.append(UsuarioController.extract(node_u.path))
        return usuarios

    def __extract_acessos_from_dataset(self, usuarios):
        acessos = []
        for usuario in usuarios:
            acessos.extend(AcessoController.extract(usuario.path))
        return acessos