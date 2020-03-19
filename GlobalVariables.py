#!/usr/bin/env python
import argparse
import os
import sys
import os.path


help_text = '''
        Ошибка! Запуск без первого обязательного аргумента...
        
  Первый обязательный аргумент определяет режим выполнения программы.
   Список аргументов:
     1.camera - поиск лиц с камеры
     2.video  - поиск лиц в видеофайле
     3.all    - поиск всех лиц в с изображениями
     4.person - поиск определенного лица в папке  с изображениями
     5.create - создание БД из подготовленных данных
     6.add    - добавление подготовленных данных в базу
     7.train  - обучение БД
     8.remove - удаление определенных данных из базы
     9.rename - переименовывание файлов в заданный формат
            '''
class GetArgs(argparse.ArgumentParser):
    def __init__(self):
        home_script = os.path.dirname(__file__)
        # создание родительского парсера
        super(GetArgs, self).__init__()
        self.pars = argparse.ArgumentParser(description='Image comparaison script', epilog='Подразумевается,\
                                                    что файл с каскадом лежит в той же директорие, что\
                                                    и весь код, иначе надо указывать полный путь к каскаду.')
        self.pars.set_defaults(command=None, db=None, 
                               cascade=None, src=None,
                               saveto=None, _show=0, 
                               ctrl=None, conf=90.0, 
                               dataname=None,
                               dbname=None, idd=0 )
        
        
        # создание субпарсера
        sub = self.pars.add_subparsers(help='Команды задающие режим выполнения.\
                                        Являются первым обязательным аргументом.',
                                                                  title='Commands')
        
        
        # режим интерактивной консоли
        console = sub.add_parser('console', help = 'Режим интерактивной консоли', 
                                     description = 'Режим интерактивной консоли.' )
        console.set_defaults(command='console', db=None, 
                             cascade=None, src=None,
                             saveto=None, _show=0, 
                             ctrl=None, conf=90.0, 
                             dataname=None,
                             dbname=None, idd=0 )
        
        # режим вебкамеры
        camera = sub.add_parser('camera', help='Режим поиска с камеры',
                                  description='Режим поиска с камеры.'  )
        camera.set_defaults(command='camera')
        camera.add_argument('db', type=str, help='Полный путь к базе данных.')
        camera.add_argument('-c', dest='cascade', type=str, 
                                  default=home_script+'/haarcascade_frontalface_default.xml',
                                                 help='Полный путь к файлу каскада, если он\
                                                       находится в другой директории.' )
        
        # режим видеофайла
        video = sub.add_parser('video', help='Режим поиска в видеофайле.')
        video.set_defaults(command='video')
        video.add_argument('db', type=str, help='Полный путь к базе данных.')
        video.add_argument('-c', dest='cascade', type=str, 
                           default=home_script+'/haarcascade_frontalface_default.xml',
                           help = 'Полный путь к файлу каскада, если он\
                                        находится в другой директории.'  )
        video.add_argument('--src', dest='src', type=str, help='Полный путь к видеофайлу.')
        
        # режим поиска всех лиц
        allface = sub.add_parser('all', help='Режим поиска всех лиц на изображениях в заданной директории.')
        allface.set_defaults(command='allface')
        allface.add_argument('--saveto', dest='saveto', type=str, help='Полный путь к папке сохранения,\
                                                                  если она не существует,добавить имя в путь')
        allface.add_argument('-s', dest='_show', type=int, default=0,
                                                 help='Флаг вывода изхображения. Если больше 0 -\
                                                       изображение выводится. По умолчанию 0')
        allface.add_argument('-c', dest='cascade', type=str, default=home_script+'/haarcascade_frontalface_default.xml',
                                                   help='Полный путь к файлу каскада, если он\
                                                         находится в другой директории.')
        allface.add_argument('--src', dest='src', type=str, help='Полный путь к изображениям.')
        
        
        # режим поиска определенного лица
        person = sub.add_parser('person', help='Режим поиска определенного лица на изображениях\
                                                в заданной директории.')
        person.set_defaults(command='person')
        person.add_argument('--saveto', dest='saveto', type=str, help='Полный путь к папке сохранения,\
                                                                  если она не существует,добавить имя в путь')
        person.add_argument('-s', dest='_show', type=int, default=0,
                                                 help='Флаг вывода изхображения. Если больше 0 -\
                                                       изображение выводится. По умолчанию 0')
        person.add_argument('-c', dest='cascade', type=str, default=home_script+'/haarcascade_frontalface_default.xml',
                                                   help='Полный путь к файлу каскада, если он\
                                                         находится в другой директории.')
        person.add_argument('--src', dest='src', type=str, help='Полный путь к изображениям.')
        person.add_argument('--ctrl', dest='ctrl', type=str, help='Полный путь к конторольным \
                                                                   изобрфжениям')
        person.add_argument('--conf', dest='conf', type=float, default=90.0,
                                                   help='Задается параметр точности поиска.\
                                                         По умолчанию 90.0')
        
        
        # создание БД
        createdb = sub.add_parser('create', help='Режим создания базы данных из подготовленных изображений.\
                                                  После рекомендуется обучить полученную базу.')
        createdb.set_defaults(command='create')
        createdb.add_argument('db', type=str, help='Полный путь к базе данных.')
        createdb.add_argument('--src', dest='src', type=str, help='Полный путь к изображениям.')
        createdb.add_argument('--dataname', dest='dataname', type=str, help='Имя для данных.')
        createdb.add_argument('--dbname', dest='dbname', type=str, help='Имя базы данных.')
        createdb.add_argument('--id', dest='idd', type=int, help='ID данных')
        
        # обучение БД
        train = sub.add_parser('train', help='Режим обучения подготовенной базы данных.')
        train.set_defaults(command='train')
        train.add_argument('db', type=str, help='Полный путь к базе данных.')
        train.add_argument('--dataname', dest='dataname', type=str, help='Имя для yml файла.')
        
        # добавление новых данных
        add_data = sub.add_parser('add', help='Режим добавления данных в базу.\
                                              После рекомендуется обучить обновленную базу.')
        add_data.set_defaults(command='add')
        add_data.add_argument('db', type=str, help='Полный путь к базе данных.')
        add_data.add_argument('--src', dest='src', type=str, help='Полный путь к изображениям.')
        add_data.add_argument('--dataname', dest='dataname', type=str, help='Имя для данных.')
        add_data.add_argument('--id', dest='idd', type=int, help='ID данных')
        
        
        # удаление данных
        del_data = sub.add_parser('remove', help='Режим удаления данных из базы по имени или id данных.')
        del_data.set_defaults(command='remove')
        del_data.add_argument('db', type=str, help='Полный путь к базе данных.')
        del_data.add_argument('--dataname', dest='dataname', type=str, help='Имя для данных.')
        del_data.add_argument('--id', dest='idd', type=int, help='ID данных')
        
        
        # переименновывание файлов в заданный формат
        rename_data = sub.add_parser('rename', help='Режим переименновывания файлов в определенный формат,\
                                                     имя_данных.id_данных.номер.jpg.')
        rename_data.set_defaults(command='rename')
        rename_data.add_argument('--src', dest='src', type=str, help='Полный путь к изображениям.')
        rename_data.add_argument('--dataname', dest='dataname', type=str, help='Имя для данных.')
        rename_data.add_argument('--id', dest='idd', type=int, help='ID данных')
        
        
        # вывод в консоль данных БД
        show_data = sub.add_parser('show', help='Режим просмотра базы данных.')
        show_data.set_defaults(command='show')
        show_data.add_argument('db', type=str, help='Полный путь к базе данных.')
        
        
        
        self.args       =  self.pars.parse_args()
        self.home       =  home_script
        self.command    =  self.args.command
        self.path_to_db =  self.args.db
        self.cascade    =  self.args.cascade
        self.src        =  self.args.src
        self.saveto     =  self.args.saveto
        self._show      =  self.args._show
        self.control    =  self.args.ctrl
        self.conf       =  self.args.conf
        self.dataname   =  self.args.dataname
        self.dbname     =  self.args.dbname
        self.idd        =  self.args.idd

    def get_help(self):
        print(help_text)















