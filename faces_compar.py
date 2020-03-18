#!/usr/bin/env python3

import os
import sys
import os.path


import GlobalVariables as gvars
import scaner_face
import DatabaseHelper as dbh


if __name__ == '__main__':
    # получение данных из командной строки
    args = gvars.GetArgs()
    print()
    # выбор режима выполнения
    command = args.command
    
    # режим камеры
    if command == 'camera':
        scaner_face.camera_scaner(args.path_to_db, args.cascade)
    
    # поиск всех лиц в папке с изображениями
    elif command == 'allface':
        state = False
        if args._show > 0:
            state = True
        # если state True то изображение выводится
        # пути должны быть полными
        scaner_face.find_all_faces(args.src, args.saveto, state, args.cascade)
    
    # поиск конкретных лиц в папке с изображениями
    elif command == 'person':
        state = False
        if args._show > 0:
            state = True
        scaner_face.find_person_face(args.src, args.saveto, args.control,
                                         confid=args.conf, show=state,
                                         cascade=args.cascade)
    
    # создание базы данных из уже подготовленных изображений
    elif command == 'create':
        dbh.create_new_db(args.dbname, args.path_to_db, args.src, args.dataname, args.idd)
    
    # добавление новых подготовленных изображений в базу
    elif command == 'add':
        dbh.add_to_db_new_files(args.src, args.path_to_db, args.dataname, args.idd)
    
    # переименовывание файлов в вид: имя_данных.id_данных.номер.jpg
    elif command == 'rename':
        dbh.rename_files(args.src, args.dataname, args.idd)
    
    # удаление определенных данных по id или имени данных
    elif command == 'remove':
            dbh.delete_data(args.path_to_db, args.dataname, args.idd)
    
    # вывод в консоль содержимого базы данных
    elif command == 'show':
            dbh.show_database(args.path_to_db)
    
    # обучение базы данных с созданием yml файла
    # если файл существует, то он удаляется и создается заново
    # с тем же или новым именем
    elif command == 'train':
            try:
                scaner_face.trains(args.path_to_db, args.dataname)
            except:
                print('Введены не верные параметры или не введены.')
                
                
# =====================================================================
    elif command == 'console':
        
        mode = ['camera',
                'allface',
                'person',
                'create',
                'add',
                'remove',
                'rename',
                'show',
                'train',
                'q', ]

        home       =  os.path.dirname(__file__)
        dbname     =  None
        path_to_db =  None
        src        =  None
        saveto     =  None
        _show      =  False
        control    =  None
        dataname   =  None
        idd        =  0
        conf       =  90.0
        
        print(' '*10, '='*40, 'Interacnive console', '='*40)
        while True:
            cascade = home+'/haarcascade_frontalface_default.xml'
            print(cascade)
            if not os.path.exists(cascade):
                cascade = None
            command = input('Команда режима выполнения:')
            if command not in mode:
                print('Команда', command, 'не найдена.')
                print('Список доступных команд:')
                for i, cmd in enumerate(mode):
                    print(str(i+1)+'.', cmd)
                continue
            
            if command == 'q':
                break
            
            if command == 'camera':
                while True:
                    if path_to_db == None:
                        path_to_db = input('Полный путь к БД:  ')
                        if not os.path.exists(path_to_db):
                            path_to_db = None
                            print('Не верный путь к БД или она не создана.')
                            continue
                    if cascade == None:
                        cascade = input('Поный путь к каскаду:  ')
                        if not os.path.exists(cascade):
                            cascade = None
                            print('Не верный путь к каскаду.')
                            continue
                    if path_to_db != None and cascade != None:
                        break
                print(cascade)
                scaner_face.camera_scaner(path_to_db, cascade)
                continue
                
            elif command == 'allface':
                state = None
                while True:
                    if src == None:
                        src = input('Полный путь к изображениям:  ')
                        if not os.path.exists(src):
                            src = None
                            print('Не верный путь к папке или она не создана.')
                            continue
                    if cascade == None:
                        cascade = input('Поный путь к каскаду:  ')
                        if not os.path.exists(cascade):
                            cascade = None
                            print('Не верный путь к каскаду.')
                            continue
                    if saveto == None:
                        saveto = input('Полный путь к папке сохранения:  ')
                        os.makedirs(saveto, exist_ok=True)
                    
                    state = input('Выводить изображения(y/n): ')
                    if state == 'y' or state == 'Y':
                        _show = True
                    elif state == 'n' or state == 'N':
                        _show = False
                    else:
                        continue
                    if src != None and cascade != None and saveto != None:
                        break
                scaner_face.find_all_faces(src, saveto, _show, cascade)
                src = None
                cascade = None
                _show = False
                saveto = None
                continue
            
            elif command == 'person':
                state = None
                while True:
                    if src == None:
                        src = input('Полный путь до изображений: ')
                        if not os.path.exists(src):
                            print(src, ' не найдено.')
                            src = None
                            continue
                    if control == None:
                        control = input('Полный путь до контрольных изображений: ')
                        if not os.path.exists(control):
                            print('Контрольные изображения не найдены.')
                            control = None
                            continue
                    if cascade == None:
                        cascade = input('Полный путь до каскада: ')
                        if not os.path.exists(cascade):
                            print('Каскад не найден.')
                            cascade = None
                            continue
                    if saveto == None:
                        saveto = input('Полный путь до папки сохранения, если не существует,создается: ')
                        os.makedirs(saveto, exist_ok=True)
                    try:
                        conf = float(input('Порог точности: '))
                    except:
                        print('Не корректный ввод...')
                        conf = 90.0
                        continue
                    state = input('Выводиить изображение(y/n):  ')
                    if state == 'y' or state == 'Y':
                        _show = True
                    elif state == 'n' or state == 'N':
                        _show = False
                    else:
                        print('Не вернный ввод...')
                        continue
                    if src != None and saveto != None and control != None:
                        break
                scaner_face.find_person_face(src, saveto, control,confid=conf,
                                                   show=_show,cascade=cascade )
                control = None
                saveto = None
                src = None
                _show = False
                conf = 90.0
            
            elif command == 'create':
                count = 0
                req = ''
                text_list = ['enter name db', 'input path to db', 'input src', 'input idd']
                var_dict = {'dbname':None, 'ptdb':None, 'src':None, 'dataname':None, 'idd':'0'}
                while True:
                    req = input(text_list[count])
                    
                
                dbh.create_new_db(args.dbname, args.path_to_db, args.src, args.dataname, idd)
                
            elif command == 'video':
                print('Режим video пока не доступен')
    
            else:
                pass
    
    print()












