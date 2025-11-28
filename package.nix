{ pkgs, ... }:
pkgs.stdenvNoCC.mkDerivation {
  name = "cursor_win2lin";

  src = ./.;

  nativeBuildInputs = with pkgs; [
    makeWrapper
  ];

  buildInputs = with pkgs; [
    python3
  ];

  postPatch = ''
    patchShebangs cursor_map.py
  '';

  installPhase = ''
    mkdir -p $out/libexec/cursor_win2lin
    cp cursor_map.py $out/libexec/cursor_win2lin/main.py
    cp mappings.txt $out/libexec/cursor_win2lin/mappings.txt
    mkdir -p $out/bin
      makeShellWrapper $out/libexec/cursor_win2lin/main.py $out/bin/cursor_win2lin \
      --prefix PATH : ${pkgs.python3}/bin \
      --set CURSOR_WIN2LIN_MAPPINGS "$out/libexec/cursor_win2lin/mappings.txt"

    runHook postInstall
  '';
}