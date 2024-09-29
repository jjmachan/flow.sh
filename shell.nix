{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    (python3.withPackages (ps: with ps; [
      # Add your Python packages here, for example:
      numpy
      pandas
      requests
    ]))
  ];

  shellHook = ''
    echo "Welcome to your Nix Python environment!"
    python --version
  '';
}
