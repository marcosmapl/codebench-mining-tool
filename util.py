# -*- coding: utf-8 -*-
### Codebench Dataset Extractor by Marcos Lima (marcos.lima@icomp.ufam.edu.br)
### Universidade Federal do Amazonas - UFAM
### Instituto de Computação - IComp

import logging
import os
from datetime import datetime


class StringUtil:

    abc = ''


class Logger:

    __path = os.path.join(os.getcwd(), 'logs')
    __cblogger = None

    @staticmethod
    def configure():
        logging.basicConfig(level=logging.INFO)

        if not os.path.exists(Logger.__path):
            os.mkdir(Logger.__path)

        formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s]: %(message)s')
        data_hoje = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        if not Logger.__cblogger:
            Logger.__cblogger = logging.getLogger('cblogger')

            ifh = logging.FileHandler(os.path.join(Logger.__path, f'{data_hoje}_info.log'))
            ifh.setLevel(level=logging.INFO)
            ifh.setFormatter(formatter)
            Logger.__cblogger.addHandler(ifh)

            wfh = logging.FileHandler(os.path.join(Logger.__path, f'{data_hoje}_warn.log'))
            wfh.setLevel(level=logging.WARNING)
            wfh.setFormatter(formatter)
            Logger.__cblogger.addHandler(wfh)

            efh = logging.FileHandler(os.path.join(Logger.__path, f'{data_hoje}_error.log'))
            efh.setLevel(level=logging.ERROR)
            efh.setFormatter(formatter)
            Logger.__cblogger.addHandler(efh)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(level=logging.INFO)
            console_handler.setFormatter(formatter)
            Logger.__cblogger.addHandler(console_handler)

    @staticmethod
    def info(msg: str):
        Logger.__cblogger.info(msg)

    @staticmethod
    def warn(msg: str):
        Logger.__cblogger.warning(msg)

    @staticmethod
    def error(msg: str):
        Logger.__cblogger.error(msg, exc_info=True)
