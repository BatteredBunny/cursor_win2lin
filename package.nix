{ pkgs, ... }:
pkgs.stdenv.mkDerivation {
  name = "cursor_win2lin";

  src = ./.;

  nativeBuildInputs = with pkgs; [
    makeWrapper
  ];

  buildInputs = with pkgs; [
    python3
  ];

  installPhase = ''
    runHook preInstall

    mkdir -p $out/share/cursor_win2lin $out/bin
    cp cursor_map.py $out/share/cursor_win2lin/main.py
    cp mappings.txt $out/share/cursor_win2lin/mappings.txt

    substituteInPlace $out/share/cursor_win2lin/main.py \
      --replace 'default_mappings_file = "mappings.txt"' \
                "default_mappings_file = \"$out/share/cursor_win2lin/mappings.txt\""

    makeWrapper ${pkgs.python3.interpreter} $out/bin/cursor_win2lin --add-flags "$out/share/cursor_win2lin/main.py"

    runHook postInstall
  '';
}