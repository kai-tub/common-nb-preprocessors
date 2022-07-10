# Common NB Preprocessors
> preprocessors

[![Tests](https://img.shields.io/github/workflow/status/kai-tub/common-nb-preprocessors/CI?color=dark-green&label=%20Tests)](https://github.com/kai-tub/common-nb-preprocessors//actions/workflows/main.yml)
[![MyPy Type Checker](https://img.shields.io/badge/%20type_checker-mypy-%231674b1?style=flat&color=dark-green)](http://mypy-lang.org/)
[![License](https://img.shields.io/pypi/l/common-nb-preprocessors?color=dark-green)](https://github.com/kai-tub/common-nb-preprocessors//blob/main/LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/common-nb-preprocessors)](https://pypi.org/project/common-nb-preprocessors)
[![PyPI version](https://img.shields.io/pypi/v/common-nb-preprocessors)](https://pypi.org/project/common-nb-preprocessors)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/common-nb-preprocessors?color=dark-green)](https://anaconda.org/conda-forge/common-nb-preprocessors)
[![Auto Release](https://img.shields.io/badge/release-auto.svg?colorA=888888&colorB=9B065A&label=auto&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAACzElEQVR4AYXBW2iVBQAA4O+/nLlLO9NM7JSXasko2ASZMaKyhRKEDH2ohxHVWy6EiIiiLOgiZG9CtdgG0VNQoJEXRogVgZYylI1skiKVITPTTtnv3M7+v8UvnG3M+r7APLIRxStn69qzqeBBrMYyBDiL4SD0VeFmRwtrkrI5IjP0F7rjzrSjvbTqwubiLZffySrhRrSghBJa8EBYY0NyLJt8bDBOtzbEY72TldQ1kRm6otana8JK3/kzN/3V/NBPU6HsNnNlZAz/ukOalb0RBJKeQnykd7LiX5Fp/YXuQlfUuhXbg8Di5GL9jbXFq/tLa86PpxPhAPrwCYaiorS8L/uuPJh1hZFbcR8mewrx0d7JShr3F7pNW4vX0GRakKWVk7taDq7uPvFWw8YkMcPVb+vfvfRZ1i7zqFwjtmFouL72y6C/0L0Ie3GvaQXRyYVB3YZNE32/+A/D9bVLcRB3yw3hkRCdaDUtFl6Ykr20aaLvKoqIXUdbMj6GFzAmdxfWx9iIRrkDr1f27cFONGMUo/gRI/jNbIMYxJOoR1cY0OGaVPb5z9mlKbyJP/EsdmIXvsFmM7Ql42nEblX3xI1BbYbTkXCqRnxUbgzPo4T7sQBNeBG7zbAiDI8nWfZDhQWYCG4PFr+HMBQ6l5VPJybeRyJXwsdYJ/cRnlJV0yB4ZlUYtFQIkMZnst8fRrPcKezHCblz2IInMIkPzbbyb9mW42nWInc2xmE0y61AJ06oGsXL5rcOK1UdCbEXiVwNXsEy/6+EbaiVG8eeEAfxvaoSBnCH61uOD7BS1Ul8ESHBKWxCrdyd6EYNKihgEVrwOAbQruoytuBYIFfAc3gVN6iawhjKyNCEpYhVJXgbOzARyaU4hCtYizq5EI1YgiUoIlT1B7ZjByqmRWYbwtdYjoWoN7+LOIQefIqKawLzK6ID69GGpQgwhhEcwGGUzfEPAiPqsCXadFsAAAAASUVORK5CYII=)](https://github.com/intuit/auto)

This repository contains a personal collection of common notebook preprocessors.
As of writing, the most relevant function is probably:
`common_nb_preprocessors.metadata_injector.jupyter_book_metadata_injector`

This function can be used to automatically inject [JupyterBook](https://jupyterbook.org/intro.html) specific tags into code-cells by using _magical_ comments.
Set the function in the [nb_custom_formats](https://jupyterbook.org/file-types/jupytext.html) entry:

```yaml
sphinx:
  config:
    nb_custom_formats:
        # as of now, this will raise an error because this option doesn't overwrite the default behaviour
        # See: https://github.com/executablebooks/jupyter-book/issues/1586
        .ipynb:
            - common_nb_preprocessors.metadata_injector.jupyter_book_metadata_injector
            # Currently, requires an option argument to work
            - remove_line: True
```
