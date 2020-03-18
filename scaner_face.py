#!/usr/bin/env python
import cv2
import os
import sys
import numpy as np
from PIL import Image
from pprint import pprint

import GlobalVariables as gvar
import DatabaseHelper as dbh

args = gvar.GetArgs()

def find_all_faces(path_to_img = None, path_to_save = None, show = False,
                    cascade = args.home+'/'+'haarcascade_frontalface_default.xml'):
    os.makedirs(path_to_save, exist_ok=True)
    file_list = dbh.sort_files(path_to_img, ['.jpg', '.png'])
    face_cascade = None
    resize_const = 800
    if len(file_list) == 0:
        print('Искомых файлов в директории не найдено.')
        return 0
    try:
        face_cascade = cv2.CascadeClassifier(cascade)
    except:
        print('Ошибка... [', cascade, '] не найден')
    if show:
        cv2.namedWindow('original', cv2.WINDOW_NORMAL)
        cv2.namedWindow('faces', cv2.WINDOW_NORMAL)
    for img_name in file_list:
        original = cv2.imread(img_name)
        if show:
            cv2.imshow('original', original)
            key = cv2.waitKey(30)
            if key == 27 or key == 13:
                cv2.destroyAllWindows()
                return 0
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
        print('Find faces:', len(faces))
        count = 0
        for (x,y,w,h) in faces:
            count += 1
            face_img = original[y:y+h, x:x+w]
            if show:
                cv2.imshow('faces', face_img)
                key = cv2.waitKey(30)
                if key == 27 or key == 13:
                    cv2.destroyAllWindows()
                    return 0
            name = path_to_save+'/'+str(count)+'_'+os.path.basename(img_name)
            cv2.imwrite(name, face_img)
            print('Saving ', name)
    if show:
        cv2.destroyAllWindows()
    return 0


def find_person_face(path_to_img = None, path_to_save = None, path_to_contr = None, confid = 90.0,
                     show = False, cascade = args.home+'/'+'haarcascade_frontalface_default.xml'):
    label_id = 0
    ids = list()
    datas = list()
    contr_list = dbh.sort_files(path_to_contr, ['.jpg', '.png'])
    os.makedirs(path_to_save, exist_ok=True)
    file_list = dbh.sort_files(path_to_img, ['.jpg', '.png'])
    face_cascade = None
    resize_const = 800
    
    if len(file_list) == 0:
        print('Искомых файлов в директории не найдено.')
        return 0
    try:
        face_cascade = cv2.CascadeClassifier(cascade)
    except:
        print('Ошибка... [', cascade, '] не найден')
    
    if show:
        cv2.namedWindow('Controls images', cv2.WINDOW_NORMAL)
    
    for name_img in contr_list:
        original_contr = cv2.imread(name_img)
        gray = cv2.cvtColor(original_contr, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3,minSize=(30,30))
        for (x,y,w,h) in faces:
            datas.append(gray[y:y+h, x:x+w])
            ids.append(label_id)
            label_id += 1
            if show:
                cv2.imshow('Controls images', gray[y:y+h, x:x+w])
                cv2.waitKey(50)
    if show:
        cv2.destroyAllWindows()
    
    recognizer  = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(datas, np.array(ids))
    
    if show:
        cv2.namedWindow('original', cv2.WINDOW_NORMAL)
        cv2.namedWindow('saving', cv2.WINDOW_NORMAL)
    
    for img_name in file_list:
        original = cv2.imread(img_name)
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
        if show:
            cv2.imshow('original', original)
            key = cv2.waitKey(50)
            if key == 27:
                cv2.destroyAllwindows()
                return
        gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4,minSize=(30,30))
        for (x,y,w,h) in faces:
            num, conf = recognizer.predict(gray[y:y+h, x:x+w])
            print('Num:', num, '  Conf:', round(conf, 5))
            if conf <= confid:
                cv2.imwrite(path_to_save+'/'+'person_'+os.path.basename(img_name), original[y:y+h, x:x+w])
                print('Saving '+'person_'+os.path.basename(img_name), 'to', path_to_save)
                if show:
                    cv2.imshow('saving', original[y:y+h, x:x+w])
                    key = cv2.waitKey(50)
                    if key == 27:
                        cv2.destroyAllwindows()
                        return
    if show:
        cv2.destroyAllWindows()


def trains(path_to_db = None, name_train = None):
    recognizer  = cv2.face.LBPHFaceRecognizer_create()
    home = os.getcwd()
    os.chdir(path_to_db)
    file_list = os.listdir(os.getcwd())
    faces = []
    labels = []
    ids = 0
    ymls = list()
    for img_file in file_list:
        if img_file.endswith('.jpg'):
            ids = int(os.path.split(img_file)[-1].split(".")[1])
            print(img_file)
            original = cv2.imread(img_file)
            image = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
            faces.append(image)
            labels.append(ids)
        if img_file.endswith('.yml'):
            if img_file != name_train:
                print('Delete ', img_file)
                os.remove(img_file)
    print('Начало обучения...')
    recognizer.train(faces, np.array(labels))
    recognizer.write(name_train)
    os.chdir(home)
    print('Обучение закончено.')
    input('Press enter...')


def camera_scaner(path_to_db = None, cascade = args.home+'/'+'haarcascade_frontalface_default.xml'):
    font = cv2.FONT_HERSHEY_SIMPLEX
    recognizer  = cv2.face.LBPHFaceRecognizer_create()
    home = os.getcwd()
    ymls = dbh.sort_files(path_to_db, ['.yml'])
    if len(ymls) == 0:
        print('Нет тренировочного файла')
        return -1
    print('Ymls: ', ymls)
    if not os.path.isfile(cascade):
        print('Ошибка.', cascade, 'не найден.')
        return -1
    face_cascade = cv2.CascadeClassifier(cascade)
    #os.chdir(path_to_db)
    recognizer.read(ymls[0])
    label = ''
    names = dbh.get_list_names(path_to_db)
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






















