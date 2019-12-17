import os
import sys
from pathlib import Path



class csvMod(object):

    

    def __init__(self, *args, **kwargs):

        super(csvMod, self).__init__(*args, **kwargs)
        self.extChanged = []

    def change_extension(self, filename):
        
        for f in filename:
            p = Path(os.path.dirname(f))
            newFile = Path(p.parent.as_posix() + '/' + p.stem + '.csv')
            self.extChanged.append(newFile)
        
        return self.extChanged

    def check_extension(self, filename):

        for f in filename:
            if Path(f).suffix == '.csv':
                continue
            else:
                Path(f).stem + '.csv'