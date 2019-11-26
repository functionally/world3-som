#!/usr/bin/env nix-shell
#!nix-shell -i "gawk -f" -p gawk

BEGIN {
  xmin = 1e10
  xmax = -1e10
  ymin = 1e10
  ymax = -1e10
  zmin = 1e10
  zmax = -1e10
  cmin = 1e10
  cmax = -1e10
}

NR > 1 && NR <= 20001 {
  i = $1

  x[i] = $21
  if ($21 < xmin)
    xmin = $21
  if ($21 > xmax)
    xmax = $21

  y[i] = $22
  if ($22 < ymin)
    ymin = $22
  if ($22 > ymax)
    ymax = $22

  z[i] = $23
  if ($23 < zmin)
    zmin = $23
  if ($23 > zmax)
    zmax = $23

  c[i] = $15
  if ($15 < cmin)
    cmin = $15
  if ($15 > cmax)
    cmax = $15
}

END {
  print "upsert {"
  print "  fram: " frame
  print "  iden: " (1000000 + frame)
  print "  type: 4"
  print "  mask: 15"
  print "  cnts: 3"
  print "  posx: 0.1"
  print "  posx: 1.0"
  print "  posx: 0.1"
  print "  posy: -0.1"
  print "  posy: -0.1"
  print "  posy: 1.0"
  print "  posz: 0.0"
  print "  posz: 0.0"
  print "  posz: 0.0"
  print "  size: 0.10"
  print "  colr: 55613088"
  print "  text: \"" name "\""
  print "}"
  for (i in x) {
    print "upsert {"
    print "  fram: " frame
    print "  iden: " i
    print "  type: 1"
    print "  mask: 15"
    print "  cnts: 1"
    print "  posx: " ((x[i] - xmin) / (xmax - xmin))
    print "  posy: " ((y[i] - ymin) / (ymax - ymin))
    print "  posz: " ((z[i] - zmin) / (zmax - zmin))
    print "  size: 0.0025"
    print "  colr: " (4278204415 - 16776960 * int(200 * (c[i] - cmin) / (cmax - cmin)))
    print "  text: \"Sim " i "\""
    print "}"
  }
}
