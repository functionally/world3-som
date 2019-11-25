#!/usr/bin/env nix-shell
#!nix-shell -p gawk -i "gawk -f"

BEGIN {
  FS = "\t"
  OFS = "\t"
}

NR > 1 {
  for (i = 3; i <= 9; ++i) {
    if ($i == "")
      $i = save[i]
    else
      save[i] = $i
  }
}

$2 != "" {
  print
}
