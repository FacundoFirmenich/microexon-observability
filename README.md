# Microexon Observability

Reproducibility tools for fragment-resolved microexon audits. The unit of comparison is a fixed fragment identity within a declared event and condition. The software distinguishes unchanged totals from retention and replacement of identities.

## Run

```sh
python -m unittest discover -s tests -v
python audit_transitions.py baseline.json comparison.json
```

Each input is a JSON object mapping fragment IDs to one decision (`true`, `false`, or `null` for not evaluable). Both inputs must contain exactly the same identities. `null` is not zero. Output contains the four paired transitions, counts of gains/losses and the identities excluded from the paired denominator. Inputs to this tool are already-adjudicated decisions, not reads or alignments. Run separate audits for inclusion, skipping, recovery in any reported alignment and unique primary recovery. Do not pool overlapping strata as independent replicates.

The public initialization contains no manuscript, private evidence or raw sequence data. It does not implement an aligner, establish molecular sensitivity or reproduce the entire study. Original software: MIT. Upstream tools retain their own terms.
