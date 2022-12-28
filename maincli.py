#!/usr/bin/env python3
from pathlib import Path

from rich import print

import arguments
import scaner_face
import datafiles

"""
Сначала необходимо найти изображения лиц на фото в какой нибудь папке.(команда find)
Затем вручную нужно отфильтровать изображения, оставив только лица одного человека.
Переименовать оставшиеся изображения в формат - имя_id_номер.расширение(команда rename)
"""


if __name__ == '__main__':
    ...
    
    args = arguments.GetArgs()
    args = args.args
    
    if args.command == 'find':
        # поиск лиц на изображениях в заданной папке с сохранением
        # изображений лиц в заданной папке
        path_to_imgs = args.src
        path_to_save = args.save
        new_size = args.size
        out_size = args.outsize
        cascade = args.cascade
        minsize = args.minsize
        scaleFactor = args.scalefactor
        minNeighbors = args.minneighbors
        scaner_face.find_all_faces(path_to_imgs, 
                                   path_to_save, 
                                   new_size=new_size,
                                   cascade=cascade,
                                   min_out_size=out_size,
                                   scaleFactor=scaleFactor,
                                   minNeighbors=minNeighbors)
    elif args.command == 'rename':
        # переименовывание изображений в определенный формат
        ...
    
    elif args.command == 'train':
        # обучение по заранее подготовленным изображениям лиц
        ...











