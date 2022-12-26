#!/usr/bin/env python
import cv2
import os
import sys
import numpy as np
from PIL import Image
from rich import print, inspect
from pathlib import Path

import arguments as gvar
import datafiles



def get_modified_size(y:int, x:int, new_size:int):
    # перерасчет размера изображения с учетом пропорциональности
    try:
        if x > y:
            dim = x / y
            x = new_size
            y = x / dim
        else:
            dim = y / x
            y = new_size
            x = y / dim
    except:
        pass
    return int(x), int(y)


def find_all_faces(path_to_imgs, 
                   path_to_save=None, 
                   new_size=800,
                   cascade = 'haarcascade_frontalface_default.xml', 
                   **kwargs):
    # поиск лиц на изображениях в заданной директории 
    # и сохранение в изображений лиц отдельную папку
    """
поиск лиц на изображениях в заданной директории 
и сохранение в изображений лиц отдельную папку
==========================================================================
   path_to_imgs: str или Path - путь к папке с исходными изображениями
   path_to_save: str или Path - путь куда сохранять изображения лиц
   new_size: int - новый размер исходного изображения. большая сторона 
                   изображения приводится к этому размеру, другая сторона
                   пропрционально высчитывается и уменьшается
   cascade: str или Path - путь до нужного каскада
   
  В kwargs:
   scaleFactor: float
   minNeighbors: int
   minSize: tuple
   min_out_size: int - минимальный размер изображений найденых лиц
                       если размер меньше, то меняется до этого параметра
    """
    scaleFactor = kwargs.get('scaleFactor', 1.1)
    minNeighbors = kwargs.get('minNeighbors', 4)
    minSize = kwargs.get('minSize', (30, 30))
    min_out_size = kwargs.get('min_out_size', 96)
    
    path_to_save = Path(__file__).resolve().parent / 'FACES' \
                        if not path_to_save else Path(path_to_save) 
    path_to_save.mkdir(parents=True, exist_ok=True)
    file_list = datafiles.filter_files(path_to_imgs, '.jpg', '.png')
    cascade_class = None
    resize_const = new_size
    CNT = 0
    if not file_list:
        print('Искомых файлов в директории не найдено.')
        return
    
    cascade_class = cv2.CascadeClassifier(cascade)
    
    for img_name in file_list:
        original = cv2.imread(str(img_name))
        
        xs, ys = get_modified_size(*original.shape[:2], resize_const)
        original = cv2.resize(original, (xs, ys), cv2.INTER_AREA)
        gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        faces = cascade_class.detectMultiScale(gray, 
                                               scaleFactor=scaleFactor, 
                                               minNeighbors=minNeighbors,
                                               minSize=minSize)
        print(f'Найдено лиц: {len(faces)}')
        count = 0
        for (x,y,w,h) in faces:
            count += 1
            CNT += 1
            face_img = original[y:y+h, x:x+w]
            if face_img.shape[0] < min_out_size:
                face_img = cv2.resize(face_img, (min_out_size, min_out_size), cv2.INTER_AREA)
            name = path_to_save / f'{CNT}_{count}{img_name.suffix}'
            cv2.imwrite(str(name), face_img)
            print('Saving ', name)


def find_person_face(path_to_img, path_to_save, path_to_contr, confid = 90.0,
                     cascade = 'haarcascade_frontalface_default.xml'):
    label_id = 0
    ids = list()
    datas = list()
    contr_list = datafiles.filter_files(path_to_contr, '.jpg', '.png')
    os.makedirs(path_to_save, exist_ok=True)
    file_list = datafiles.filter_files(path_to_img, '.jpg', '.png')
    face_cascade = None
    resize_const = 800
    
    if not file_list:
        print('Искомых файлов в директории не найдено.')
        return
    
    face_cascade = cv2.CascadeClassifier(cascade)
    
    for name_img in contr_list:
        original_contr = cv2.imread(str(name_img))
        gray = cv2.cvtColor(original_contr, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3,minSize=(30,30))
        for (x,y,w,h) in faces:
            datas.append(gray[y:y+h, x:x+w])
            ids.append(label_id)
            label_id += 1
    
    recognizer  = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(datas, np.array(ids))
    
    for img_name in file_list:
        original = cv2.imread(str(img_name))
        s = original.shape
        ys = s[0] 
        xs = s[1] 
        if xs > resize_const and xs > ys:
            dim = xs / resize_const
            xs = resize_const
            ys = int(ys / dim)
        elif ys > resize_const and ys > xs:
            dim = ys / resize_const
            ys = resize_const
            xs = int(xs / dim)
        else:
            pass
        original = cv2.resize(original, (xs, ys), cv2.INTER_AREA)
        gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4,minSize=(30,30))
        for (x,y,w,h) in faces:
            num, conf = recognizer.predict(gray[y:y+h, x:x+w])
            print('Num:', num, '  Conf:', round(conf, 5))
            if conf <= confid:
                cv2.imwrite(path_to_save+'/'+'person_'+os.path.basename(img_name), original[y:y+h, x:x+w])
                print('Saving '+'person_'+os.path.basename(img_name), 'to', path_to_save)


def trains(path_to_imgs, filename_train = None):
    # обучение по изображениям лиц. название должно соответствовать
    # формату {имя объекта}_{id}_{номер}.расширение
    # 
    recognizer  = cv2.face.LBPHFaceRecognizer_create()
    path_to_imgs = Path(path_to_imgs)
    file_list = datafiles.filter_files(path_to_imgs, '.jpg', '.png', '.yml')
    faces = []
    labels = []
    ids = 0
    for img_file in file_list:
        if img_file.suffix in ('.jpg', '.png') and datafiles.is_valid_name(img_file.name):
            ids = int(img_file.stem.split('_')[1])
            print(img_file)
            original = cv2.imread(str(img_file))
            image = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
            faces.append(image)
            labels.append(ids)
    print('Начало обучения...')
    recognizer.train(faces, np.array(labels))
    recognizer.write(filename_train)
    print('Обучение закончено.')


def camera_scaner(path_to_db = None, cascade = 'haarcascade_frontalface_default.xml'):
    font = cv2.FONT_HERSHEY_SIMPLEX
    recognizer  = cv2.face.LBPHFaceRecognizer_create()
    ymls = datafiles.filter_files(path_to_db, '.yml')
    if len(ymls) == 0:
        raise Exception('Нет тренировочного файла')
    print('Ymls: ', ymls)
    face_cascade = cv2.CascadeClassifier(cascade)
    #os.chdir(path_to_db)
    recognizer.read(str(ymls[0]))
    label = ''
    names = datafiles.get_list_names(path_to_db)
    num = 0
    cap = cv2.VideoCapture(0)
    #cap.set(cv2.CAP_PROP_FPS, 10)
    cv2.namedWindow('video')
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.35, minNeighbors=4,minSize=(30,30))
        
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,100,25), 3)
            
            num, conf = recognizer.predict(gray[y:y+h, x:x+w])
            if conf < 100:
                label = names[num]
                info  = "  {0}%".format(round(100 - conf))
                #print('Num:', num, ' Conf:', conf)
            else:
                label = "unknown"
                info = "  {0}%".format(round(100 - conf))
        
            cv2.putText(frame, str(label), (x + 5, y - 5), font, 1, (25, 55, 255), 3)
            cv2.putText(frame, str(info), (x + 5, y + h + 30), font, 1, (5, 5, 255), 3)
        cv2.imshow('video', frame)
        key = cv2.waitKey(1)
        if key == 27 or key == 13:
            cap.release()
            cv2.destroyAllWindows()
            break 

    cap.release()
    cv2.destroyAllWindows()






if __name__ == "__main__":
    ...
    
    # inspect(inspect, all=True)
    # find_all_faces('/home/baron/images/DCIM/ya/', path_to_save='./ya', scaleFactor=1.3)
    # datafiles.rename_files('/home/baron/Coding/MyPython/faces_recogn/ya/', 1, 'baron', '.jpg', '.png')
    # trains('/home/baron/Coding/MyPython/faces_recogn/ya/', 'train.yml')
    
    camera_scaner('/home/baron/Coding/MyPython/faces_recogn/ya/')
    
    # origin = cv2.imread('/home/baron/images/DCIM/priroda/IMG_20220110_120651.jpg')
    # xs, ys = get_modified_size(*origin.shape[:2], 600)
    # origin = cv2.resize(origin, (xs, ys), cv2.INTER_AREA)
    # cv2.imshow('test', origin)
    # cv2.waitKey(0)












