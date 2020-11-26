#!/usr/bin/env python
# coding: utf-8

# In[1]:


__author__ = 'wankw (wankaiweii@gamil.com)' 

import os
import pyautogui as pag
pag.FAILSAFE = False #PyAutoGUI fail-safe triggered from mouse moving to a corner of the screen.
import time
import win32gui
from shutil import copy

vesta_path = r'E:\Academic_Software\VESTA-win64\VESTA-win64\VESTA.exe'
button_image_path = r'E:\System\Desktop\AVD\button_image'
maxtrytime = 15


# In[2]:


def open_vesta():
    os.popen(f'{vesta_path}')
    time.sleep(4)
    handle = win32gui.FindWindow(None, 'VESTA')
    left, top, right, bottom = win32gui.GetWindowRect(handle)
    title_pos = (left+100, top+10)
       
    #move to (0,0) upper left of main screen
    pag.moveTo(title_pos)
    pag.dragTo(0,0,0.5,button='left')
    pag.hotkey('alt','space','x')
    


# In[3]:


def click_button(button_figure,click=1):
    time_start=time.time()
    button = pag.locateOnScreen(button_figure, grayscale=True,confidence=0.9)
    while not button:
        button = pag.locateOnScreen(button_figure, grayscale=True,confidence=0.9)
        time_end=time.time()
        if time_end - time_start >= maxtrytime:
            print (f'{os.path.basename(button_figure).replace(".png", "")} error, wrong VESTA version or UI!')
            os._exit(0)
    button_position = pag.center(button) 
    pag.click(button_position,clicks=click,interval=0.05)
    
def click_button_left(button_figure,click=1):
    time_start=time.time()
    button = pag.locateOnScreen(button_figure, grayscale=True,confidence=0.9)
    while not button:
        button = pag.locateOnScreen(button_figure, grayscale=True,confidence=0.9)
        time_end=time.time()
        if time_end - time_start >= maxtrytime:
            print (f'{os.path.basename(button_figure).replace(".png", "")} error, wrong VESTA version or UI!')
            os._exit(0)
    pag.click((button[0], button[1]+button[3]/2),clicks=click,interval=0.05)


# In[5]:


def export_raster_image(filename,tifname):
    click_button(rf'{button_image_path}\zoom_in.png',click=7)
    click_button_left(rf'{button_image_path}\space_filling.png')
    
    #side view
    click_button(rf'{button_image_path}\a.png')
    click_button(rf'{button_image_path}\file.png')
    click_button(rf'{button_image_path}\export_raster.png')  
    pag.hotkey('ctrl','a')
    pag.typewrite(f'{tifname}-{filename}-side.tif') 
    click_button(rf'{button_image_path}\export_raster_save.png')
    click_button_left(rf'{button_image_path}\export_raster_transparent.png')    
    click_button(rf'{button_image_path}\export_raster_ok.png')
    pag.press(['enter'])
    
    #top view
    click_button(rf'{button_image_path}\c.png')
    click_button(rf'{button_image_path}\file.png')
    click_button(rf'{button_image_path}\export_raster.png')
    pag.hotkey('ctrl','a')
    pag.typewrite(f'{tifname}-{filename}-top.tif') 
    click_button(rf'{button_image_path}\export_raster_save.png')
    click_button_left(rf'{button_image_path}\export_raster_transparent.png') 
    click_button(rf'{button_image_path}\export_raster_ok.png')
    pag.press(['enter'])
    
    pag.hotkey('ctrl','w')


# In[6]:


def draw_vesta_figure(filename,tifname):    
    #export raster image
    os.popen(f'{vesta_path} {filename}')
    export_raster_image(filename,tifname)
    print ('VESTA draw successfully!')


# In[38]:


def draw_in_all_folders(path_list, filename):
    ori_path = os.getcwd()
    open_vesta()
    
    for path in path_list:
        os.chdir(path)
        print (f'{path}:  ',end='')
        tifname = os.path.basename(path)
        draw_vesta_figure(filename,tifname)
        
        if not os.path.isfile(fr'{ori_path}\{tifname}-{filename}-side.tif'):
            copy(fr'{path}\{tifname}-{filename}-side.tif',fr'{ori_path}\{tifname}-{filename}-side.tif')
        else:
            path_name = path.replace('\\',' ').replace(':', '')
            copy(fr'{path}\{tifname}-{filename}-side.tif',fr'{ori_path}\{path_name}-{filename}-side.tif')  
        if not os.path.isfile(fr'{ori_path}\{tifname}-{filename}-top.tif'):
            copy(fr'{path}\{tifname}-{filename}-top.tif',fr'{ori_path}\{tifname}-{filename}-top.tif')
        else:
            path_name = path.replace('\\',' ').replace(':', '')
            copy(fr'{path}\{tifname}-{filename}-top.tif',fr'{ori_path}\{path_name}-{filename}-top.tif') 


# In[8]:


def get_path_list_from_file(dir_file,filename):
    path_list = []
    with open(dir_file) as file:
        for line in file.readlines():
            path = line.replace('\n','')
            if os.path.isfile(fr'{path}\{filename}'):
                path_list.append(path)
    return path_list


# In[9]:


def get_all_folder_path_list(filename):
    dir = os.getcwd()
    path_list = []
    
    for path, dir_list, file_list in os.walk(dir):
        for dir_name in dir_list:
            whole_path = os.path.join(path, dir_name)
            if os.path.isfile(fr'{whole_path}\{filename}'):
                path_list.append(whole_path)
                
    return path_list


# In[10]:


def get_subfolder_path_list(filename):
    dir = os.getcwd()
    path_list = []

    for path in os.listdir(dir):
        if os.path.isfile(fr'{path}\{filename}'):
            whole_path = os.path.join(dir,path)
            if os.path.isfile(fr'{whole_path}\{filename}'):
                path_list.append(whole_path)
            
    return path_list


# In[42]:


def get_version():
    return '1.0 (2020.11.26, wankaiweii@gamil.com)'


# In[ ]:


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Draw vaspcar file or cif file by VESTA automatically.')
    parser.add_argument('-v', '--version', action='version', version=get_version(),help='Display version')
    parser.add_argument('-f','--input_filename', type=str, action='store', default='CONTCAR',
                        help='The name of file you want to draw. [Optional] [default=CONTCAR] ')
    #Add conflicted option.
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-df','--dir_file', type=str, action='store',
                       help='Conflicts with -w -l option. The input file with the path list of folder you want to draw (One line writes one path). [Optional]')
    group.add_argument('-w','--walk', action='store_true', default=False,
                       help='Conflicts with -df -l option. Traverse all folders (depth=max) in the current working directory. [Optional] [default=False] ')
    group.add_argument('-l','--loop_through', action='store_true', default=False,
                       help='Conflicts with -df -w option. Loop through all subfolders (depth=1) under the current folder. [Optional] [default=False] ')
    
    args = parser.parse_args()

    if args.dir_file != None:
        print ('Directory file mode.')
        path_list = get_path_list_from_file(args.dir_file,args.input_filename)
        draw_in_all_folders(path_list,args.input_filename)
        pag.hotkey('ctrl','w')
    
    elif args.walk == True:
        print ('Walk mode.')
        path_list = get_all_folder_path_list(args.input_filename)
        draw_in_all_folders(path_list,args.input_filename)
        pag.hotkey('ctrl','w')
        
    elif args.loop_through == True:
        print ('Loop through mode.')
        path_list = get_subfolder_path_list(args.input_filename)
        draw_in_all_folders(path_list,args.input_filename)
        pag.hotkey('ctrl','w')
    
    else:
        print ('Current directory mode.')
        tifname = os.path.basename(os.getcwd())
        open_vesta()
        draw_vesta_figure(args.input_filename,tifname)
        pag.hotkey('ctrl','w')

