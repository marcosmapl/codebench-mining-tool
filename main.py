# -*- coding: utf-8 -*-
### Codebench Dataset Extractor by Marcos Lima (marcos.lima@icomp.ufam.edu.br)
### Universidade Federal do Amazonas - UFAM
### Instituto de Computação - IComp

import os

from miner import CodebenchMiner
from util import Logger
from view import MainScreen

__version__ = '3.2.0'

if __name__ == '__main__':
    # configura o módulo de log
    Logger.configure()
    # cria a pasta para os arquivos de saídade (CSV), caso já exista, recria os arquivos
    CodebenchMiner.create_output_dir()
    # inicia a tela principal da aplicação
    MainScreen('Codebench Extration Tool', __version__, 900, 450)
