# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, "API_VERSION", (0, 9)) < (0, 11):
    raise Exception(
        "Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s"
        % (kaitaistruct.__version__)
    )


class MtkDbgInfo(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        super(MtkDbgInfo, self).__init__(_io)
        self._parent = _parent
        self._root = _root or self
        self._read()

    def _read(self):
        self.magic = self._io.read_bytes(8)
        if not self.magic == b"\x43\x41\x54\x49\x43\x54\x4e\x52":
            raise kaitaistruct.ValidationNotEqualError(
                b"\x43\x41\x54\x49\x43\x54\x4e\x52", self.magic, self._io, "/seq/0"
            )
        self.version = self._io.read_u2le()
        self.sub_version = self._io.read_u2le()
        self.db_offset = self._io.read_u4le()

    def _fetch_instances(self):
        pass
        _ = self.databases
        if hasattr(self, "_m_databases"):
            pass
            for i in range(len(self._m_databases)):
                pass
                self._m_databases[i]._fetch_instances()

        _ = self.db_count
        if hasattr(self, "_m_db_count"):
            pass

    class Database(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(MtkDbgInfo.Database, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(4)
            if not self.magic == b"\x43\x41\x54\x49":
                raise kaitaistruct.ValidationNotEqualError(
                    b"\x43\x41\x54\x49", self.magic, self._io, "/types/database/seq/0"
                )
            self.version = self._io.read_u4le()
            self.sub_version = self._io.read_u4le()
            self.project_name = (self._io.read_bytes_term(0, False, True, True)).decode(
                "UTF-8"
            )
            self.hw_version = (self._io.read_bytes_term(0, False, True, True)).decode(
                "UTF-8"
            )
            self.sw_version = (self._io.read_bytes_term(0, False, True, True)).decode(
                "UTF-8"
            )
            self.build_time = (self._io.read_bytes_term(0, False, True, True)).decode(
                "UTF-8"
            )
            self.symbol_table_rel_offset = self._io.read_u4le()
            self.file_table_rel_offset = self._io.read_u4le()

        def _fetch_instances(self):
            pass
            _ = self.file_table
            if hasattr(self, "_m_file_table"):
                pass
                self._m_file_table._fetch_instances()

            _ = self.symbol_table
            if hasattr(self, "_m_symbol_table"):
                pass
                self._m_symbol_table._fetch_instances()

        @property
        def abs_file_table_offset(self):
            if hasattr(self, "_m_abs_file_table_offset"):
                return self._m_abs_file_table_offset

            self._m_abs_file_table_offset = self.ori_offset + self.file_table_rel_offset
            return getattr(self, "_m_abs_file_table_offset", None)

        @property
        def abs_symbol_table_offset(self):
            if hasattr(self, "_m_abs_symbol_table_offset"):
                return self._m_abs_symbol_table_offset

            self._m_abs_symbol_table_offset = (
                self.ori_offset + self.symbol_table_rel_offset
            )
            return getattr(self, "_m_abs_symbol_table_offset", None)

        @property
        def file_table(self):
            if hasattr(self, "_m_file_table"):
                return self._m_file_table

            _pos = self._io.pos()
            self._io.seek(self.abs_file_table_offset)
            self._m_file_table = MtkDbgInfo.FileTable(
                self.version, self._io, self, self._root
            )
            self._io.seek(_pos)
            return getattr(self, "_m_file_table", None)

        @property
        def ori_offset(self):
            if hasattr(self, "_m_ori_offset"):
                return self._m_ori_offset

            self._m_ori_offset = self._parent.offset
            return getattr(self, "_m_ori_offset", None)

        @property
        def symbol_table(self):
            if hasattr(self, "_m_symbol_table"):
                return self._m_symbol_table

            _pos = self._io.pos()
            self._io.seek(self.abs_symbol_table_offset)
            self._m_symbol_table = MtkDbgInfo.SymbolTable(self._io, self, self._root)
            self._io.seek(_pos)
            return getattr(self, "_m_symbol_table", None)

    class DatabaseContainer(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(MtkDbgInfo.DatabaseContainer, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.offset = self._io.read_u4le()
            self.name = (self._io.read_bytes_term(0, False, True, True)).decode("UTF-8")
            self.trace_tag = (self._io.read_bytes_term(0, False, True, True)).decode(
                "UTF-8"
            )

        def _fetch_instances(self):
            pass
            _ = self.database
            if hasattr(self, "_m_database"):
                pass
                self._m_database._fetch_instances()

        @property
        def database(self):
            if hasattr(self, "_m_database"):
                return self._m_database

            _pos = self._io.pos()
            self._io.seek(self.offset)
            self._m_database = MtkDbgInfo.Database(self._io, self, self._root)
            self._io.seek(_pos)
            return getattr(self, "_m_database", None)

    class FileEntry(KaitaiStruct):
        def __init__(self, version, _io, _parent=None, _root=None):
            super(MtkDbgInfo.FileEntry, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self.version = version
            self._read()

        def _read(self):
            self.filepath = (self._io.read_bytes_term(0, False, True, True)).decode(
                "UTF-8"
            )
            if self.filepath != "":
                pass
                self.count = self._io.read_u4le()

            if self.filepath != "":
                pass
                self.ranges = []
                for i in range(self.count):
                    self.ranges.append(
                        MtkDbgInfo.RangeEntry(self.version, self._io, self, self._root)
                    )

        def _fetch_instances(self):
            pass
            if self.filepath != "":
                pass

            if self.filepath != "":
                pass
                for i in range(len(self.ranges)):
                    pass
                    self.ranges[i]._fetch_instances()

    class FileTable(KaitaiStruct):
        def __init__(self, version, _io, _parent=None, _root=None):
            super(MtkDbgInfo.FileTable, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self.version = version
            self._read()

        def _read(self):
            self.entries = []
            i = 0
            while True:
                _ = MtkDbgInfo.FileEntry(self.version, self._io, self, self._root)
                self.entries.append(_)
                if _.filepath == "":
                    break
                i += 1

        def _fetch_instances(self):
            pass
            for i in range(len(self.entries)):
                pass
                self.entries[i]._fetch_instances()

    class RangeEntry(KaitaiStruct):
        def __init__(self, version, _io, _parent=None, _root=None):
            super(MtkDbgInfo.RangeEntry, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self.version = version
            self._read()

        def _read(self):
            self.start_address = self._io.read_u4le()
            self.end_address = self._io.read_u4le()
            if self.version >= 2:
                pass
                self.line_number = self._io.read_u4le()

        def _fetch_instances(self):
            pass
            if self.version >= 2:
                pass

    class SymbolEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(MtkDbgInfo.SymbolEntry, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.name = (self._io.read_bytes_term(0, False, True, True)).decode("UTF-8")
            self.start_address = self._io.read_u4le()
            self.end_address = self._io.read_u4le()

        def _fetch_instances(self):
            pass

    class SymbolTable(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(MtkDbgInfo.SymbolTable, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.entries = []
            i = 0
            while True:
                _ = MtkDbgInfo.SymbolEntry(self._io, self, self._root)
                self.entries.append(_)
                if _.name == "":
                    break
                i += 1

        def _fetch_instances(self):
            pass
            for i in range(len(self.entries)):
                pass
                self.entries[i]._fetch_instances()

    @property
    def databases(self):
        if hasattr(self, "_m_databases"):
            return self._m_databases

        _pos = self._io.pos()
        self._io.seek(self.db_offset + 4)
        self._m_databases = []
        for i in range(self.db_count):
            self._m_databases.append(
                MtkDbgInfo.DatabaseContainer(self._io, self, self._root)
            )

        self._io.seek(_pos)
        return getattr(self, "_m_databases", None)

    @property
    def db_count(self):
        if hasattr(self, "_m_db_count"):
            return self._m_db_count

        _pos = self._io.pos()
        self._io.seek(self.db_offset)
        self._m_db_count = self._io.read_u4le()
        self._io.seek(_pos)
        return getattr(self, "_m_db_count", None)
