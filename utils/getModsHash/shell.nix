{ pkgs ? import <nixpkgs> { } }:
pkgs.mkShell {
  packages = with pkgs; [
    (python312.withPackages (p: with p; [
      requests
    ]))
  ];
}
