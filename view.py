# -*- coding: utf-8 -*-
### Codebench Dataset Extractor by Marcos Lima (marcos.lima@icomp.ufam.edu.br)
### Universidade Federal do Amazonas - UFAM
### Instituto de Computação - IComp
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from miner import CodebenchMiner
from util import Logger


class MainScreen(tk.Tk):

    COLOR_DARK_GREEN = '#062315'
    COLOR_DARK_GRAY = '#444444'
    COLOR_CYPRUS = '#06373A'
    COLOR_EDEN = '#1F5F5B'
    COLOR_SOLEM = '#159947'
    COLOR_OCEAN_GREEN = '#49B265'
    COLOR_PASTEL_GRAY = '#CAD2C5'
    COLOR_BACKGROUND = COLOR_DARK_GRAY
    COLOR_FOREGROUND = COLOR_PASTEL_GRAY

    def __init__(self, name: str, version: str, screen_width: int, screen_height: int):
        super().__init__()
        # configurações básicas da interface
        self.name = name
        self.version = version
        self.title(string=f'{name} v{version}')

        # width x height (comprimento x altura)
        self.window_width = screen_width
        self.window_height = screen_height
        self.geometry(f"{screen_width}x{screen_height}")
        self.resizable(False, False)

        # configurações de aparência
        self.configure(background=MainScreen.COLOR_BACKGROUND)
        self.estilo = ttk.Style(self)
        self.estilo.configure('cbminer.label.TLabel', background=MainScreen.COLOR_BACKGROUND, foreground=MainScreen.COLOR_FOREGROUND)

        self.dataset_path = tk.StringVar(self)

        self.lbl_codebench_path = ttk.Label(master=self, text='INSIRA O CAMINHO PARA O DATASET CODEBENCH: ', style='cbminer.label.TLabel')
        self.lbl_codebench_path.place(x=25, y=25)
        self.ent_codebench_path = tk.Entry(master=self, width=105, textvariable=self.dataset_path)
        self.ent_codebench_path.place(x=25, y=60)

        self.frm_opcoes = tk.LabelFrame(master=self, text='OPÇÕES DE EXTRAÇÃO   ', bg=MainScreen.COLOR_BACKGROUND, fg=MainScreen.COLOR_FOREGROUND)
        self.frm_opcoes.place(x=25, y=105, width=850, height=240)

        self.var_extrair_social = tk.BooleanVar()
        self.check_social = tk.Checkbutton(
            self.frm_opcoes, 
            text='DADOS SOCIAIS', 
            variable=self.var_extrair_social, 
            onvalue=True, 
            offvalue=False, 
            bg=MainScreen.COLOR_BACKGROUND, 
            fg=MainScreen.COLOR_FOREGROUND, 
            highlightbackground=MainScreen.COLOR_BACKGROUND, 
            activebackground=MainScreen.COLOR_BACKGROUND, 
            activeforeground=MainScreen.COLOR_OCEAN_GREEN, 
            selectcolor=MainScreen.COLOR_OCEAN_GREEN
        )
        self.check_social.place(x=15, y=15)

        self.var_extrair_tentativas = tk.BooleanVar()
        self.check_tentativas = tk.Checkbutton(
            self.frm_opcoes, 
            text='DADOS DAS TENTATIVAS', 
            variable=self.var_extrair_tentativas, 
            onvalue=True, 
            offvalue=False, 
            bg=MainScreen.COLOR_BACKGROUND, 
            fg=MainScreen.COLOR_FOREGROUND, 
            highlightbackground=MainScreen.COLOR_BACKGROUND, 
            activebackground=MainScreen.COLOR_BACKGROUND, 
            activeforeground=MainScreen.COLOR_OCEAN_GREEN, 
            selectcolor=MainScreen.COLOR_OCEAN_GREEN
        )
        self.check_tentativas.place(x=15, y=40)

        self.var_extrair_metricas = tk.BooleanVar()
        self.check_metricas = tk.Checkbutton(
            self.frm_opcoes, 
            text='DADOS MÉTRIACAS DE CÓDIGO', 
            variable=self.var_extrair_metricas, 
            onvalue=True, 
            offvalue=False, 
            bg=MainScreen.COLOR_BACKGROUND, 
            fg=MainScreen.COLOR_FOREGROUND, 
            highlightbackground=MainScreen.COLOR_BACKGROUND, 
            activebackground=MainScreen.COLOR_BACKGROUND, 
            activeforeground=MainScreen.COLOR_OCEAN_GREEN, 
            selectcolor=MainScreen.COLOR_OCEAN_GREEN
        )
        self.check_metricas.place(x=15, y=65)

        self.var_extrair_mousemove = tk.BooleanVar()
        self.check_mousemove = tk.Checkbutton(
            self.frm_opcoes, 
            text='DADOS EVENTOS DO MOUSE', 
            variable=self.var_extrair_mousemove, 
            onvalue=True, 
            offvalue=False, 
            bg=MainScreen.COLOR_BACKGROUND, 
            fg=MainScreen.COLOR_FOREGROUND, 
            highlightbackground=MainScreen.COLOR_BACKGROUND, 
            activebackground=MainScreen.COLOR_BACKGROUND, 
            activeforeground=MainScreen.COLOR_OCEAN_GREEN, 
            selectcolor=MainScreen.COLOR_OCEAN_GREEN
        )
        self.check_mousemove.place(x=15, y=90)

        self.btn_extrair = tk.Button(master=self, text='EXTRAIR', command=self.btn_extrair_click, font=('Arial', 24), bg=MainScreen.COLOR_EDEN, foreground=MainScreen.COLOR_PASTEL_GRAY, activeforeground=MainScreen.COLOR_EDEN)
        self.btn_extrair.place(x=700, y=360)

        self.progress_string = tk.StringVar()
        self.progress_string.set('Progresso...')
        self.progress_lb = tk.Label(self, textvariable=self.progress_string)
        self.progress_lb.pack(side=tk.BOTTOM, fill=tk.X)

        self.mainloop()

    def get_dataset_path(self):
        return self.dataset_path.get()

    def btn_extrair_click(self):
        opcoes = dict()
        opcoes[CodebenchMiner.OPTION_SOCIAL_DATA] = self.var_extrair_social.get()
        opcoes[CodebenchMiner.OPTION_TENTATIVAS_DATA] = self.var_extrair_tentativas.get()
        opcoes[CodebenchMiner.OPTION_METRICAS_DATA] = self.var_extrair_metricas.get()
        opcoes[CodebenchMiner.OPTION_MOUSEMOVE_DATA] = self.var_extrair_mousemove.get()
        print("OPCOESSSSSSSSSSSSSSSSSSSSSSSSSS", opcoes)
        CodebenchMiner.extract(self.get_dataset_path(), opcoes)

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
                            try:
                                tentativas.extend(TentativaController.extract(node_ex.path))
                            except Exception as err:
                                Logger.error(str(err))
                # with os.scandir(os.path.join(usuario.path, CodeMirrorController.get_codemirror_folder_name())) as nodes_m:
                #     for node_m in nodes_m:
                #         if node_m.is_file():
                #             Logger.info(f'Extraindo logs do codemirror do arquivo: {node_ex.path}')
                #             try:
                #                 # codemirror.extend(CodeMirrorController.extract(node_m.path))
                #             except Exception as err:
                #                 Logger.error(str(err))
                with os.scandir(os.path.join(usuario.path, NotaController.get_grade_folder_name())) as nodes_g:
                    for node_g in nodes_g:
                        if node_g.is_file() and not node_g.name.startswith('final_grade'):
                            Logger.info(f'Extraindo notas do arquivo: {node_g.path}')
                            try:
                                notas.append(NotaController.extract(node_g.path))
                            except Exception as err:
                                Logger.error(str(err))
            TentativaController.persist(tentativas)
            # CodeMirrorController.persist(codemirror)
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