#!/usr/bin/env nix-shell
#!nix-shell -I nixpkgs=https://github.com/NixOS/nixpkgs/archive/d5291756487d70bc336e33512a9baf9fa1788faf.tar.gz -i python shell.nix


from tucker_tsne import analyze

analyze(
	"sensitivity-01",
	"Simulation",
	"Time",
	[
          "initial nonrenewable resources"
        , "land life policy implementation time"
        , "technology development delay"
        , "fertility control effectiveness time"
        , "zero population growth time"
        , "industrial output per capita desired"
        , "industrial equilibrium time"
        ],
	[5, 10, 20],    # times
	[5, 7],         # metrics
	[30, 100, 300], # perplexities,
	25000           # runs
)
