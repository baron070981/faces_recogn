#!/usr/bin/env python
import os
import sys
import shutil
from rich import print
import re
import os.path
from pathlib import Path



def gcd(ret_type=None):
    if ret_type is None:
        return Path(__file__).resolve().parent
    return str(Path(__file__).resolve().parent)


def filter_files(path_to_files, *exts):
    # выбирает из заданной директории файлы с задаными расширениями
    path_to_files = Path(path_to_files)
    file_list = path_to_files.iterdir()
    file_list = list(filter(lambda x: x.suffix in exts, file_list))
    return file_list


def rename_file(path_to_file, idf, newname, count, *exts):
    ptf = Path(path_to_file)
    if ptf.suffix not in exts:
        return
    name = ptf.parent / f'{newname}_{idf}_{count+1}{ptf.suffix}'
    ptf.rename(name)


def rename_files(path_to_files, idf, newname, *exts):
    # переименовывает в заданной директории файлы
    # с заданными расширениями
    count = 0
    files = filter_files(path_to_files, *exts)
    for f in files:
        name = f.parent / f'{newname}_{idf}_{count}{f.suffix}'
        f.rename(name)
        count += 1


def is_valid_name(string):
    # проверка соответствия имени файла
    sp = string.split('_')
    if len(sp) != 3 or len(sp[-1].split('.')) != 2:
        return False
    name, idf, cnt = sp
    cnt = cnt.split('.')[0].isdigit()
    idf = idf.isdigit()
    return name and cnt and idf


# была create_new_db
def create_dir_for_datas(path_db, dir_name, **kwargs):
    # создание 
    count = 0
    path_db = Path(path_db) / dir_name
    path_to_files = kwargs.get('path_to_files')
    if not path_to_files:
        return
    path_to_files = Path(path_to_files)
    file_list = list(path_to_files.iterdir())
    file_list = list(filter(lambda x: is_valid_name(x.name), file_list))
    for f in file_list:
        newname = path_db / f.name
        shutil.copyfile(str(f), str(newname))
    


def add_to_db_new_files(src, path_to_save, new_name, idd):
    '''
 src -------- путь к папке откуда беруться изображения
 path_to_db - путь к базе с контрольными изображениями
              база должна существовать
 new_name --- имя которое будет выводится в определении
 idd -------- id набора контрольных изображений
              если имя уже существует, то данные допишутся по его id
              если не существует, то создастся новое имя, если id еще нет в базе
              иначе завершиться с кодом -1
    '''
    
    

def get_params(path_db = None):
    ...


def delete_data(path_to_db = None, dataname = None, idd = 0):
    ...



if __name__ == '__main__':
    
    ...
    
    
    
    
    
    
    
    
    
    
    
    
    




