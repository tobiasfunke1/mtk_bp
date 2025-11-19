#!/usr/bin/env python3

import typer
from mtk_structs.mtk_dbg_info import MtkDbgInfo
from kaitaistruct import KaitaiStream


app = typer.Typer()


def file_info(file_table: MtkDbgInfo.FileTable):
    for file_entry in file_table.entries:
        file_entry: MtkDbgInfo.FileEntry

        # terminator entry
        if file_entry.filepath == '':
            break

        print(file_entry.filepath)
        for range_entry in file_entry.ranges:
            range_entry: MtkDbgInfo.RangeEntry
            print(f'\t{range_entry.start_address:#010x} - {range_entry.end_address:#010x}')


def symbol_text(symbol_table: MtkDbgInfo.SymbolTable, remap=False, as_functions=False):
    for symbol_entry in symbol_table.entries:
        symbol_entry: MtkDbgInfo.SymbolEntry

        # terminator entry
        if symbol_entry.name == '':
            break

        name = symbol_entry.name.replace(' ', '_')
        start_address = symbol_entry.start_address
        if remap and start_address < 0x90000000:
            start_address += 0x90000000

        def_type = 'f' if as_functions else 'l'

        print(f'{name} {start_address:#010x} {def_type}')


def load_dbg_info(dbg_file):
    mtk_dbg = MtkDbgInfo(KaitaiStream(dbg_file))
    return mtk_dbg


@app.command()
def files(dbg_file: typer.FileBinaryRead):
    mtk_dbg = load_dbg_info(dbg_file)
    container = mtk_dbg.container

    for i, database_container in enumerate(container.databases):
        database_container: MtkDbgInfo.DatabaseContainer
        database: MtkDbgInfo.Database = database_container.database

        print(f'# {database_container.offset:#08x} {database_container.name} {database_container.trace_tag}')
        file_info(database.file_table)


@app.command()
def symbols(dbg_file: typer.FileBinaryRead, remap: bool = False, labels: bool = False):
    mtk_dbg = load_dbg_info(dbg_file)
    container = mtk_dbg.container

    for i, database_container in enumerate(container.databases):
        database_container: MtkDbgInfo.DatabaseContainer
        database: MtkDbgInfo.Database = database_container.database

        if container.db_count > 1:
            print(f'# {database_container.offset:#08x} {database_container.name} {database_container.trace_tag}')

        symbol_text(database.symbol_table, remap=remap, as_functions=(not labels))

    if container.db_count > 1:
        print('# WARNING: output contains symbols for multiple debug info entries (separator lines begin with "#"")')


@app.command()
def info(dbg_file: typer.FileBinaryRead):
    mtk_dbg = load_dbg_info(dbg_file)
    container = mtk_dbg.container

    for i, database_container in enumerate(container.databases):
        database_container: MtkDbgInfo.DatabaseContainer
        database: MtkDbgInfo.Database = database_container.database

        file_table = database.file_table.entries
        symbol_table = database.symbol_table.entries

        assert file_table[-1].filepath == ''
        assert symbol_table[-1].name == ''

        print(f'{i:2d}: {database_container.offset:#08x} {database_container.name} {database_container.trace_tag}:\t{len(file_table) - 1} files, {len(symbol_table) - 1} symbols')


if __name__ == '__main__':
    app()
