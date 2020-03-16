#!/usr/bin/env python3

import os
import sys
import os.path


import GlobalVariables as gvars
import scaner_face
import DatabaseHelper as dbh


if __name__ == '__main__':
    args = gvars.GetArgs()
    print()
    command = args.command
    if command == 'camera':
        scaner_face.camera_scaner(args.path_to_db, args.cascade)
    
    elif command == 'allface':
        state = False
        if args._show > 0:
            state = True
        scaner_face.find_all_faces(args.src, args.saveto, state, args.cascade)
    
    elif command == 'person':
        state = False
        if args._show > 0:
            state = True
        scaner_face.find_person_face(args.src, args.saveto, args.control,
                                         confid=args.conf, show=state,
                                         cascade=args.cascade)
    
    elif command == 'create':
        dbh.create_new_db(args.dbname, args.path_to_db, args.src, args.dataname, args.idd)
    
    elif command == 'add':
        dbh.add_to_db_new_files(args.src, args.path_to_db, args.dataname, args.idd)
    
    elif command == 'rename':
        dbh.rename_files(args.src, args.dataname, args.idd)
    
    elif command == 'remove':
            dbh.delete_data(args.path_to_db, args.dataname, args.idd)
    
    elif command == 'show':
            dbh.show_database(args.path_to_db)
    
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

        home = os.path.dirname(__file__)
        print(home)
        path_to_db = None
        src = None
        saveto = None
        _show = False
        
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
        
        
        
        
        
        
# =====================================================================
    
    
    
    
    
    else:
        print('Режим video пока не доступен')
    
    print()












