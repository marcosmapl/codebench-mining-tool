# -*- coding: utf-8 -*-
### Codebench Dataset Extractor by Marcos Lima (marcos.lima@icomp.ufam.edu.br)
### Universidade Federal do Amazonas - UFAM
### Instituto de Computação - IComp

import miner
import util
import view

__version__ = '3.3.0'

if __name__ == '__main__':
    # configura o módulo de log
    util.Logger.configure()
    # cria a pasta para os arquivos de saídade (CSV), caso já exista, recria os arquivos
    miner.CodebenchMiner.create_output_dir()
    # inicia a tela principal da aplicação
    view.MainScreen('Codebench Extration Tool', __version__, 900, 450)
