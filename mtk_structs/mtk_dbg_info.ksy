meta:
  id: mtk_dbg_info
  file-extension: mtk_dbg_info
  encoding: UTF-8
  endian: le

seq:
  - id: container
    type: databases_container

types:

  databases_container:
    seq:
      - id: magic
        contents: "CATICTNR"
      - id: version
        type: u2
      - id: sub_version
        type: u2
      - id: db_offset
        type: u4

    instances:
      db_count:
        pos: db_offset
        type: u4

      databases:
        pos: db_offset+4
        type: database_container
        repeat: expr
        repeat-expr: db_count

  database_container:
    seq:
      - id: offset
        type: u4
      - id: name
        type: strz
      - id: trace_tag
        type: strz

    instances:
      database:
        pos: offset
        type: database

  database:
    seq:
      - id: magic
        contents: "CATI"
      - id: version
        type: u4
      - id: sub_version
        type: u4
      - id: project_name
        type: strz
      - id: hw_version
        type: strz
      - id: sw_version
        type: strz
      - id: build_time
        type: strz
      - id: symbol_table_rel_offset
        type: u4
      - id: file_table_rel_offset
        type: u4

    instances:
      ori_offset:
        value: _parent.offset
      abs_symbol_table_offset:
        value: ori_offset + symbol_table_rel_offset
      abs_file_table_offset:
        value: ori_offset + file_table_rel_offset
      symbol_table:
        pos: abs_symbol_table_offset
        type: symbol_table
      file_table:
        pos: abs_file_table_offset
        type: file_table(version)

  symbol_table:
    seq:
      - id: entries
        type: symbol_entry
        repeat: until
        repeat-until: _.name == ""

  symbol_entry:
    seq:
      - id: name
        type: strz
      - id: start_address
        type: u4
      - id: end_address
        type: u4

  file_table:
    params:
      - id: version
        type: u4

    seq:
      - id: entries
        type: file_entry(version)
        repeat: until
        repeat-until: _.filepath == ""

  file_entry:
    params:
      - id: version
        type: u4

    seq:
      - id: filepath
        type: strz
      - id: count
        type: u4
        if: filepath != ""
      - id: ranges
        type: range_entry(version)
        repeat: expr
        repeat-expr: count
        if: filepath != ""

  range_entry:
    params:
      - id: version
        type: u4

    seq:
      - id: start_address
        type: u4
      - id: end_address
        type: u4
      - id: line_number
        type: u4
        if: version >= 2
