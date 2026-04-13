{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = [
    pkgs.python312
    pkgs.python312Packages.pip
    pkgs.python312Packages.virtualenv
    pkgs.nodejs_22
    pkgs.sqlite
    pkgs.ruff
    pkgs.black
  ];

  shellHook = ''
    if [ ! -d .venv ]; then
      python -m venv .venv
    fi
    source .venv/bin/activate
    pip install -q -r requirements.txt
  '';
}
