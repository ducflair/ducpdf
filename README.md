# ducpdf

<p align="center">
  <br/>
  <!-- <a href="https://duc.ducflair.com" target="_blank"><img width="256px" src="https://ducflair-public.s3.eu-west-2.amazonaws.com/duc/duc-extended.png" /></a> -->
  <p align="center">Convert between DUC and PDF</p>
  <p align="center" style="align: center;">
    <a href="https://pypi.org/project/ducflair-ducpdf/"><img src="https://shields.io/badge/Pip-blue?logo=Pypi&logoColor=white&style=round-square" alt="Pip" /></a>
    <a href="https://github.com/ducflair/duc/releases"><img src="https://img.shields.io/pypi/v/ducflair-ducpdf?style=round-square&label=latest%20stable" alt="PyPI ducflair-ducpdf@latest release" /></a>
    <a href="https://pypi.org/project/ducflair-ducpdf/"><img src="https://img.shields.io/pypi/dm/ducflair-ducpdf?style=round-square&color=salmon" alt="Downloads" /></a>
    <img src="https://shields.io/badge/Python-ffde57?logo=Python&logoColor=646464&style=round-square" alt="Python" />
  </p>
</p>


# comandos

to update the dependencies or venv
```sh
uv sync
```

to run the test output
```sh
uv run -m src.ducpdf.test_duc_to_pdf "/Users/larasousa/Code/PDF_DUC/ducpdf/tests/inputs/H04-ACV-EXE-001-R02 copy.pdf"
```