"""
@Description :   
@Author      :   hisham 
@Time        :   2024/03/08 13:57:10
"""
import logging
import time
import os.path as osp
import os

import gradio as gr

existed_logger = {}

def make_or_exist(path):
    if osp.exists(path):
        pass
    else:
        os.makedirs(path)
def get_root_logger(name="sawa",log_save_path=None):
    
    # logging.getLogger("PIL").setLevel(logging.WARNING)

    if name in existed_logger:
        return existed_logger[name]
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    sh.setLevel(logging.DEBUG)
    log_name = time.strftime("%Y%m%d%H%M%S",time.localtime())+f'{name}.log'
    if log_save_path is not None:
        make_or_exist(log_save_path)
        fh = logging.FileHandler(osp.join(log_save_path,log_name))
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    logger.addHandler(sh)
    existed_logger[name]=logger


    return logger

def print_log(msg, logger, level=logging.INFO,mode = None):

    if mode is not None:
        print_log_gr(msg)
        return

    assert logger is not None
    assert isinstance(logger, logging.Logger)
    logger.log(level, msg)

def print_log_gr(msg):
    if not isinstance(msg,str):
        msg = str(msg)
    gr.Info(msg)
    

