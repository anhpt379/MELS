#! coding: utf-8
data_folder = '/home/Workspace/MobileEnglishLearning/v0.9.1/files/data'

import os

def levels(lang='en'):
    try:
        parent_folder = unicode(os.path.join(data_folder, lang))
        _levels = os.listdir(parent_folder)
        results = []
        # get only folder names
        for level in _levels:
            if os.path.isdir(os.path.join(parent_folder, level)):
                results.append(level)
        return sorted(results)
    except OSError:
        return 404

def lessons(level, lang='en'):
    try:
        parent_folder = unicode(os.path.join(data_folder, lang))
        parent_folder = os.path.join(parent_folder, level)
        _lessons = os.listdir(parent_folder)
        results = []
        for lesson in _lessons:
            if os.path.isdir(os.path.join(parent_folder, lesson)):
                results.append(lesson)
        return sorted(results)
    except OSError:
        return 404
    
def files(level, lesson, lang='en'):
    try:
        parent_folder = unicode(os.path.join(data_folder, lang, level, lesson))
        audio = os.listdir(parent_folder)
        results = []
        for i in audio:
            title = None
            description = None
            if i.endswith('.inf'):
                # add '\t' to detect end string when replace
                i = i + '\t'
                amr = os.path.join(parent_folder, i.replace('.inf\t', '.amr'))
                if not os.path.exists(amr): # check amr file exist
                    return 404
                i = i.replace('\t', '') # restore i
                # file inf chứa 2 biến là title và description
                cmd = open(os.path.join(parent_folder, i))
                exec(cmd)   # thực hiện chuỗi như là 1 lệnh
                info = {'title': title,
                        'description': description,
                        'audio_file': amr}
                results.append(info)
        return results
    except OSError:
        return 404  
    

if __name__ == '__main__':
    print levels()
    
    print '-' * 80
    
    print lessons('2. Elementary')
    
    print '-' * 80
    
    print files('2. Elementary', 'Lesson 01 - Nice to meet you!')