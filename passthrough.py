#!/usr/bin/env python

from __future__ import with_statement

import os
import sys
import errno
# MODIFIED 4/14 - Chase
import hashlib # to generate md5sums
import pickle # to handle serialization of the md5dictionary (persistence)
# END MODIFICATION

from fusepy import FUSE, FuseOSError, Operations, fuse_get_context


class Passthrough(Operations):
    def __init__(self, root):
        self.root = root
        # MODIFIED 4/14 - Chase
        self.md5_file = os.path.join(root, ".md5_hashes")

        if os.path.exists(self.md5_file):  # if the dictionary exists, load and instantiate it
           with open(self.md5_file, "rb") as file:
              self.md5dictionary = pickle.load(file)
        else: # otherwise we create a new one
           self.md5dictionary = {}
        # END MODIFICATION

    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    # MODIFIED 4/14 - Chase
    def _get_md5(self, path):
        # MODIFIED 4/20 - Quang
        if not os.path.exists(self.md5_file):  # if the dictionary exists, load and instantiate it
            print("DEBUG: .md5_hashes not found")
            self.md5dictionary = {}
        
        myhash = hashlib.md5()
        with open(path, "rb") as file:
           buffer = file.read()
           myhash.update(buffer)
        return myhash.hexdigest()

    def _update_md5(self, path):
       full_path = self._full_path(path)
       self.md5dictionary[path[1:]] = self._get_md5(full_path)
       self.save_hashes()

    def save_hashes(self):
       with open(self.md5_file, "wb") as file:
          pickle.dump(self.md5dictionary, file)
    # END MODIFICATION

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        full_path = self._full_path(path)
        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        full_path = self._full_path(path)
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        full_path = self._full_path(path)
        return os.chown(full_path, uid, gid)

    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def readdir(self, path, fh):
        full_path = self._full_path(path)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        for r in dirents:
            yield r

    def readlink(self, path):
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        return os.mkdir(self._full_path(path), mode)

    def statfs(self, path):
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def unlink(self, path):
        print("Unlink Called");
        return os.unlink(self._full_path(path))

    def symlink(self, name, target):
        return os.symlink(target, self._full_path(name))

    def rename(self, old, new):
        # MODIFIED 4/14 - Chase
        old_path = self._full_path(old)
        new_path = self._full_path(new)
        os.rename(old_path, new_path) # os.rename doesn't return anything so we can call it early
        if old[1:] in self.md5dictionary: # helper method isnt helpful...(?!)
           self.md5dictionary[new[1:]] = self.md5dictionary.pop[old[1:]]
           self.save_hashes()
        # return os.rename(self._full_path(old), self._full_path(new))
        # END MODIFICATION

    def link(self, target, name):
        # MODIFIED 4/14 - Chase
        target_path = self._full_path(target)
        name_path = self._full_path(name)
        os.link(name_path, target_path) # same as rename() here with os.link
        self._update_md5(name_path)
        # return os.link(self._full_path(name), self._full_path(target))
        # END MODIFICATION

    def utimens(self, path, times=None):
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        full_path = self._full_path(path)
        print("DEBUG: Open Called")
        # MODIFIED 4/14 - Chase
        # check the integrity before opening the file
        current_md5 = self._get_md5(full_path)
        stored_md5 = self.md5dictionary.get(path[1:])

        if stored_md5 is None: # if we don't have a hash stored for this file
           print("WARNING: No hash stored for file. Generating and storing hash.")
           self._update_md5(path)
           stored_md5 = current_md5
           print("SUCCESS: Hash generated and stored.")
        elif current_md5 != stored_md5: # if the file is "corrupted"
           print("!!!CRITICAL: FILE CORRUPTED!!!")
        else:
           print("SUCCESS: File is verified.") 
        # END MODIFICATION
        return os.open(full_path, flags)

    def create(self, path, mode, fi=None):
        uid, gid, pid = fuse_get_context()
        full_path = self._full_path(path)
        fd = os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)
        os.chown(full_path,uid,gid) #chown to context uid & gid
        # MODIFIED 4/14 - Chase
        self._update_md5(path)
        # END MODIFICATION
        return fd

    def read(self, path, length, offset, fh):
        print("DEBUG: Read Called");
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        print("DEBUG: Write Called");
        os.lseek(fh, offset, os.SEEK_SET)
        # MODIFIED 4/14 - Chase
        # need to write BEFORE we get and set the new hash (this took too long to realize)
        # os.write actually returns the # of written bytes, handling that too just in case
        written = os.write(fh, buf)
        self._update_md5(path) # we sneak in here, before write() exits but after the write is complete
        return written
        # END MODIFICATION
        # return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        full_path = self._full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)
        # MODIFIED 4/14 - Chase
        self._update_md5(path)
        # END MODIFICATION

    def flush(self, path, fh):
        return os.fsync(fh)

    def release(self, path, fh):
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        return self.flush(path, fh)


def main(mountpoint, root):
    print("FUSE initialized")
    FUSE(Passthrough(root), mountpoint, nothreads=True, foreground=True, allow_other=True)

if __name__ == '__main__':
    main(sys.argv[2], sys.argv[1])
