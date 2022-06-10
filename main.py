# -*- coding: utf-8 -*-
### Codebench Dataset Extractor by Marcos Lima (marcos.lima@icomp.ufam.edu.br)
### Universidade Federal do Amazonas - UFAM
### Instituto de Computação - IComp

import os

from controller import EntityController
from util import Logger
from view import MainScreen

__version__ = '3.0.0'
# cwd (current working dir): diretório de trabalho atual
__cwd__ = os.getcwd()

if __name__ == '__main__':
    # cria a pasta para os arquivos de saídade (CSV), caso já exista, recria os arquivos
    EntityController.create_output_dir()
    # configura o módulo de log
    Logger.configure()
    MainScreen('Codebench Extration Tool', __version__)
