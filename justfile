src_dir := justfile_dir() / 'src'
_pythonpath := env('PYTHONPATH', '')
export PYTHONPATH := if _pythonpath == '' { src_dir } else { src_dir + ':' + _pythonpath }


@_list:
  just --list --unsorted

fix:
  isort .

lint:
  ruff check
  isort . -c

type:
  pyright

[positional-arguments]
@test *args:
  pytest "${@}"

example name:
  cd examples && python -m {{name}}
