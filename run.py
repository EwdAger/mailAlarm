# coding=utf-8
"""
Created on 2020/3/26 14:37

@author: EwdAger
"""
from mail_pigeon.pigeon import Pigeon

if __name__ == "__main__":
    p = Pigeon()
    p.add_jobs()
    p.start()
