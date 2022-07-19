# Common NB Preprocessors
> A collection of common notebook preprocessors and some useful wrappers.

[![Tests](https://img.shields.io/github/workflow/status/kai-tub/common-nb-preprocessors/CI?color=dark-green&label=%20Tests)](https://github.com/kai-tub/common-nb-preprocessors//actions/workflows/main.yml)
[![Code Coverage](https://img.shields.io/badge/%20Coverage->95%25-%231674b1?style=flat&color=dark-green)](https://github.com/kai-tub/common-nb-preprocessors//blob/main/pyproject.toml)
[![License](https://img.shields.io/pypi/l/common-nb-preprocessors?color=dark-green)](https://github.com/kai-tub/common-nb-preprocessors//blob/main/LICENSE)
[![MyPy Type Checker](https://img.shields.io/badge/%20type_checker-mypy-%231674b1?style=flat&color=dark-green)](http://mypy-lang.org/)
[![Python Versions](https://img.shields.io/pypi/pyversions/common-nb-preprocessors)](https://pypi.org/project/common-nb-preprocessors)
[![PyPI version](https://img.shields.io/pypi/v/common-nb-preprocessors)](https://pypi.org/project/common-nb-preprocessors) <!-- [![Conda Version](https://img.shields.io/conda/vn/conda-forge/common-nb-preprocessors?color=dark-green)](https://anaconda.org/conda-forge/common-nb-preprocessors) -->
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)
[![Auto Release](https://img.shields.io/badge/release-auto.svg?colorA=888888&colorB=blueviolet&label=auto&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAACzElEQVR4AYXBW2iVBQAA4O+/nLlLO9NM7JSXasko2ASZMaKyhRKEDH2ohxHVWy6EiIiiLOgiZG9CtdgG0VNQoJEXRogVgZYylI1skiKVITPTTtnv3M7+v8UvnG3M+r7APLIRxStn69qzqeBBrMYyBDiL4SD0VeFmRwtrkrI5IjP0F7rjzrSjvbTqwubiLZffySrhRrSghBJa8EBYY0NyLJt8bDBOtzbEY72TldQ1kRm6otana8JK3/kzN/3V/NBPU6HsNnNlZAz/ukOalb0RBJKeQnykd7LiX5Fp/YXuQlfUuhXbg8Di5GL9jbXFq/tLa86PpxPhAPrwCYaiorS8L/uuPJh1hZFbcR8mewrx0d7JShr3F7pNW4vX0GRakKWVk7taDq7uPvFWw8YkMcPVb+vfvfRZ1i7zqFwjtmFouL72y6C/0L0Ie3GvaQXRyYVB3YZNE32/+A/D9bVLcRB3yw3hkRCdaDUtFl6Ykr20aaLvKoqIXUdbMj6GFzAmdxfWx9iIRrkDr1f27cFONGMUo/gRI/jNbIMYxJOoR1cY0OGaVPb5z9mlKbyJP/EsdmIXvsFmM7Ql42nEblX3xI1BbYbTkXCqRnxUbgzPo4T7sQBNeBG7zbAiDI8nWfZDhQWYCG4PFr+HMBQ6l5VPJybeRyJXwsdYJ/cRnlJV0yB4ZlUYtFQIkMZnst8fRrPcKezHCblz2IInMIkPzbbyb9mW42nWInc2xmE0y61AJ06oGsXL5rcOK1UdCbEXiVwNXsEy/6+EbaiVG8eeEAfxvaoSBnCH61uOD7BS1Ul8ESHBKWxCrdyd6EYNKihgEVrwOAbQruoytuBYIFfAc3gVN6iawhjKyNCEpYhVJXgbOzARyaU4hCtYizq5EI1YgiUoIlT1B7ZjByqmRWYbwtdYjoWoN7+LOIQefIqKawLzK6ID69GGpQgwhhEcwGGUzfEPAiPqsCXadFsAAAAASUVORK5CYII=)](https://github.com/intuit/auto)

You are probably here for the _useful_ wrappers 😉

These wrappers allow you to:
1. Write _magic_ comments inside of your jupyter-notebook code cells
2. Injects them as metadata
3. Returns the notebook node for further processing by [MyST-NB](https://myst-nb.readthedocs.io/en/latest/index.html)

See the [documentation](https://docs.kai-tub.tech/common-nb-preprocessors/) for more details.
