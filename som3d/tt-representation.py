#!/usr/bin/env nix-shell
#!nix-shell -i python shell.nix


from tucker_tsne import analyze

analyze(
	"data/results",
	"Run Label",
	"Year",
	[
          "actual net income"
        , "actual spending"
        , "base investor ask rate"
        , "BS assets"
        , "BS balance"
        , "BS equity"
        , "BS liabilities"
        , "Commercial Capital Cost Scaled"
        , "Commercial Capital Expense"
        , "Commercial Feedstock Cost Scaled"
        , "Commercial Fixed Operating Cost Scaled"
        , "commercial plant construction"
        , "commercial plant is built"
        , "commercial plant operation"
        , "Commercial Variable Operating Cost Scaled"
        , "Completed Demoing"
        , "Completed Piloting"
        , "Completed Research"
        , "Continuous Demoing Hours"
        , "Continuous Piloting Hours"
        , "Cumulative Demoing Production"
        , "Cumulative Feedstock Consumption"
        , "Cumulative Production"
        , "demo plant construction"
        , "demo plant is built"
        , "demoing complete"
        , "demoing ongoing"
        , "Demoing Rate"
        , "expected hypothetical net income"
        , "expected investor wait time"
        , "expected successful investor ask rate"
        , "Feedstock Price"
        , "Government Commercial Capital Grant"
        , "Government Demo Capital Grant"
        , "Government Pilot Capital Grant"
        , "hypothetical net income"
        , "hypothetical net margin"
        , "idealized NPV"
        , "investor ask rate"
        , "long term market share"
        , "long term market value"
        , "management runway response"
        , "NPV at required return"
        , "payback period"
        , "Pilot Capital Expense"
        , "pilot plant construction"
        , "pilot plant is built"
        , "piloting complete"
        , "piloting ongoing"
        , "Piloting Rate"
        , "pre-commercial"
        , "pre-demoing"
        , "pre-piloting"
        , "probability of successful investor ask"
        , "redemoing"
        , "Regulatory Costs"
        , "regulatory delay"
        , "remaining project duration"
        , "repiloting"
        , "smoothed NPV"
        , "smoothed NPV deviation fraction"
        , "startup piloting complete"
        , "Technology Readiness Level"
        , "Total Grants"
        , "Total Investment"
        , "Working Capital"
        ],
	[2, 4, 6],      # times
	[5, 10, 15],    # metrics
	[30, 100, 300], # perplexities,
	None            # runs
)

