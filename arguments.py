#!/usr/bin/env python
import argparse
from pathlib import Path


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
        # создание родительского парсера
        super(GetArgs, self).__init__()
        
        cascade = Path(__file__).resolve().parent / 'haarcascade_frontalface_default.xml'
        
        self.pars = argparse.ArgumentParser(description='Image comparaison script', epilog='Подразумевается,\
                                                    что файл с каскадом лежит в той же директорие, что\
                                                    и весь код, иначе надо указывать полный путь к каскаду.')
        
        
        # создание субпарсера
        sub = self.pars.add_subparsers(help='Команды задающие режим выполнения.\
                                        Являются первым обязательным аргументом.',
                                                                  title='Commands')
        
        find_faces = sub.add_parser('find', help='создание набора изображений. после создания изображений\
                                                  лучше вручную отфильтровать изображения, \
                                                  оставив лица только одного человека')
        find_faces.set_defaults(command='find')
        find_faces.add_argument('src', help='путь к папке с иссходными изображениями в которых будут искаться лица')
        find_faces.add_argument('save', help='путь к папке в которую будут сохранятся изображения найденых лиц')
        find_faces.add_argument('-S', '--size', type=int, help='размер к которому следует приводить\
                                размер исходного изображения перед поиском лиц', default=800)
        find_faces.add_argument('-o', '--outsize', type=int, help='минимальный размер изображений найденых лиц\
                                  если размер меньше, то меняется до этого параметра', default=96)
        find_faces.add_argument('-c', '--cascade', default=cascade)
        find_faces.add_argument('-f', '--scalefactor', type=float, default=1.3)
        find_faces.add_argument('-m', '--minneighbors', type=int, default=4)
        find_faces.add_argument('-s', '--minsize', type=tuple, default=(30,30))
        
        self.args = self.pars.parse_args()

    def get_help(self):
        print(help_text)






if __name__ == "__main__":
    ...







