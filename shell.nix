{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = [
    pkgs.python312
    pkgs.python312Packages.pip
    pkgs.python312Packages.virtualenv
    pkgs.nodejs_22
    pkgs.sqlite
    pkgs.podman-compose
    pkgs.terraform
  ];

  shellHook = ''
    if [ ! -d .venv ]; then
      python -m venv .venv
    fi
    source .venv/bin/activate
    pip install -q -r requirements.txt
    pip install -q -r requirements-dev.txt
  '';
}
