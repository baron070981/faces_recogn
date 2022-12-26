#!/usr/bin/env python
import os
import sys
import shutil
from rich import print
import re
import os.path
from pathlib import Path

# создание б.д. путь к исходн. переименовывание исходников, создание копий с новыми именами по новому пути
# 
# 
# path/to/db/name.id.count.jpg
# 


def gcd(ret_type=None):
    if ret_type is None:
        return Path(__file__).resolve().parent
    return str(Path(__file__).resolve().parent)


# def sort_files(path_to_files = None, ext_list = ['.jpg']):
    # home = os.getcwd()
    # os.chdir(path_to_files)
    # file_list = list()
    # for filename in os.listdir(os.getcwd()):
        # for ext in ext_list:
            # if filename.endswith(ext):
                # file_list.append(os.path.abspath(filename))
    # os.chdir(home)
    # return file_list


# была sort_files
def filter_files(path_to_files, *exts):
    # выбирает из заданной директории файлы с задаными расширениями
    path_to_files = Path(path_to_files)
    file_list = path_to_files.iterdir()
    file_list = list(filter(lambda x: x.suffix in exts, file_list))
    return file_list




# def rename_files(path_to_files, newname = None, ids = None):
    # count = 0
    # home = os.getcwd()
    # os.chdir(path_to_files)
    # temp_list = os.listdir(os.getcwd())
    # for name in temp_list:
        # if name.endswith('.jpg'):
            # new_name = newname+'.'+str(ids)+'.'+str(count)+'.jpg'
            # os.rename(name, new_name)
            # count += 1
    # os.chdir(home)


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


def create_new_db(db_name = None, path_db = os.getcwd(), files_path = None, name = None, idd = 0):
    count = 0
    file_list = list()
    home = os.getcwd()
    os.chdir(path_db)
    os.makedirs(db_name, exist_ok = True)
    os.chdir(db_name)
    p = os.getcwd()
    if files_path == None or name == None or idd == 0:
        print('Создана пустая папка для БД.')
        return False
    temp_list = os.listdir(files_path)
    for data in temp_list:
        if data.endswith('.jpg'):
            new_name = name+'.'+str(idd)+'.'+str(count)+'.jpg'
            shutil.copyfile(files_path+'/'+data, p+'/'+new_name)
            count += 1
    os.chdir(home)
    return True


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
def create_dir_for_datas(path_db, db_name, **kwargs):
    # создание 
    count = 0
    path_db = Path(path_db) / db_name
    # path_db.mkdir(parents=True, exist_ok=True)
    path_to_files = kwargs.get('path_to_files')
    if not path_to_files:
        return
    path_to_files = Path(path_to_files)
    file_list = list(path_to_files.iterdir())
    file_list = list(filter(lambda x: is_valid_name(x.name), file_list))
    for f in file_list:
        newname = path_db / f.name
        shutil.copyfile(str(f), str(newname))
    


def add_to_db_new_files(src = None, path_to_db = None, new_name = None, idd = 0):
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
    if src == None or path_to_db == None or new_name == None or idd == 0:
        print(add_to_db_new_files, 'Не определен один или несколько параметров')
        return -1
    pattern  = r'(\w+)[\.,_](\d+)[\.,_](\d+).\w+'
    # name: [ids, counts]
    list_db  = list()
    list_src = list()
    
    ids      = set()
    counts   = list()
    names    = dict()
    
    temp_id = idd
    temp_count = 0
    
    list_db = os.listdir(path_to_db)
    pprint(list_db)
    home = os.getcwd()
    for data in list_db:
        if data.endswith('.jpg'):
            data_split   = re.search(pattern, data)
            _name        = data_split.group(1)
            _id          = int(data_split.group(2))
            ids.add(_id)
            _count       = int(data_split.group(3))
            names[_name] = [_id, _count]
    print(names)
    
    for data in list_db:
        if data.endswith('.jpg'):
            data_split   = re.search(pattern, data)
            _name        = data_split.group(1)
            _count = int(data_split.group(3))
            count = int(names[_name][1])
            if count < _count:
                names[_name][1] = _count
    print(names)
    
    if new_name not in names and idd in ids:
        print('Id уже существует для другого имени.')
        return -1
    if new_name in names:
        temp_id = names[new_name][1]
        temp_count = names[new_name][0]
    
    os.chdir(src)
    temp_list = os.listdir(os.getcwd())
    for name in temp_list:
        if name.endswith('.jpg'):
            newname = new_name+'.'+str(temp_id)+'.'+str(temp_count)+'.jpg'
            shutil.copyfile(name, path_to_db+'/'+newname)
            temp_count += 1
    os.chdir(home)
    

def get_params_from_db(path_db = None):
    pattern  = r'(\w+)[\.,_](\d+)[\.,_](\d+).\w+'
    file_list = os.listdir(path_db)
    data_dict = dict()
    for data in file_list:
        if data.endswith('.jpg'):
            data_split = re.search(pattern, data)
            name = data_split.group(1)
            idd = int(data_split.group(2))
            data_dict[name] = idd
    return data_dict
    

def get_list_names(path_db = None):
    data_dict = get_params_from_db(path_db)
    print(data_dict)
    list_names = ['None']*(len(data_dict)+1)
    for name in data_dict:
        list_names[data_dict[name]] = name
    return list_names


def delete_data(path_to_db = None, dataname = None, idd = 0):
    pattern = r'(\w+)[\.,_](\d+)[\.,_](\d+).\w+'
    home = '/'.join(sys.argv[0].strip().split('/')[:-1])
    os.chdir(path_to_db)
    file_list = os.listdir(os.getcwd())
    name = ''
    _id = 0
    if dataname == None and idd == 0:
        print('Не введены данные для удаления.')
        return 0
    if dataname != '' and dataname != None:
        count = 0
        for _name in file_list:
            print(_name)
            name_split = re.search(pattern, _name)
            if name_split == None:
                continue
            name = name_split.group(1)
            if name == dataname:
                count += 1
                os.remove(_name)
                print('Удаление ', _name)
        print('Удаленно ', count, ' файлов')
        return 0
    else:
        count = 0
        for _name in file_list:
            print(_name)
            name_split = re.search(pattern, _name)
            if name_split != None:
                _id = int(name_split.group(2))
                if _id == idd:
                    count += 1
                    os.remove(_name)
                    print('Удаление ', _name)
        print('Удаленно ', count, ' файлов')
        return 0



def show_database(path_to_db = None):
    data_dict = get_params_from_db(path_to_db)
    file_list = os.listdir(path_to_db)
    count = 0
    for data in data_dict:
        count += 1
        print(str(count)+'.', data, ':', data_dict[data])
    for _file in file_list:
        if not _file.endswith('.jpg'):
            count += 1
            print(str(count)+'.', _file)



if __name__ == '__main__':
    
    ...
    p = Path('testdir2')
    create_dir_for_datas('/home/baron/Coding/MyPython/toportcode/', 
                         'testdir2', 
                         path_to_files='/home/baron/Coding/MyPython/toportcode/testdir/')
    
    
    
    
    
    
    
    
    
    
    
    




