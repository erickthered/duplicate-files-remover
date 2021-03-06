import sys
import os
import hashlib


class Duplitector:
    filesizes = {}
    total_files = 0
    duplicated_files = 0
    used_space = 0
    autodelete = False

    def chunk_reader(self, fobj, chunk_size=1024):
        while True:
            chunk = fobj.read(chunk_size)
            if not chunk:
                return
            yield chunk

    def get_file_hash(self, filepath, hash=hashlib.sha1):
        hashobj = hash()
        for chunk in self.chunk_reader(open(filepath, 'rb')):
            hashobj.update(chunk)

        return hashobj.digest()

    def check_for_duplicates(self, paths, hash=hashlib.sha1):
        if (paths[0] == '--delete'):
            self.autodelete = True
            paths = paths[1:]

        for path in paths:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    full_path = os.path.join(dirpath, filename)
                    filesize = os.path.getsize(full_path)
                    same_size_files = self.filesizes.get(filesize, [])
                    same_size_files.append(full_path)
                    self.filesizes[filesize] = same_size_files
                    self.total_files = self.total_files + 1

        for filesize, files in self.filesizes.items():
            if (len(files) > 1):
                file_hashes = {}
                for file in files:
                    file_hash = self.get_file_hash(file)
                    duplicate = file_hashes.get(file_hash, None)
                    if duplicate:
                        self.duplicated_files = self.duplicated_files + 1
                        self.used_space = self.used_space + filesize
                        if self.autodelete:
                            os.remove(file)
                            print "Removed ", file
                        else:
                            print "%s\n\tduplicate of:\n%s\n" % \
                                (file, duplicate)
                    else:
                        file_hashes[file_hash] = file

    def report(self):
        duplicated_percent = self.duplicated_files/(self.total_files*1.0)*100
        print "\n==============  REPORT  =============="
        print "Total files: ", self.total_files
        print "Duplicated files: ", self.duplicated_files
        print "Percentage of duplicated files: ", duplicated_percent, "%"
        if self.autodelete:
            print "Recovered disk space: ", self.used_space, " bytes"
        else:
            print "Duplicated disk space usage: ", self.used_space, " bytes"


if __name__ == '__main__':
    if sys.argv[1:]:
        d = Duplitector()
        d.check_for_duplicates(sys.argv[1:])
        d.report()
    else:
        usage = "Usage :"
        usage = usage + sys.argv[0]
        usage = usage + " [--delete] <path> [<path_2> [<path3>] ... ]"
        print usage
