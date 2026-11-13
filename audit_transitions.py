"""Count paired transitions without conflating missing evaluation with failure."""
import argparse
import json
from pathlib import Path


def unique_object(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f'duplicate fragment identity: {key}')
        out[key] = value
    return out


def audit(baseline, comparison):
    for data in (baseline, comparison):
        if not isinstance(data, dict) or any(not isinstance(k, str) or not k or
                                            (v is not None and type(v) is not bool)
                                            for k, v in data.items()):
            raise ValueError('expected a mapping of nonempty fragment IDs to booleans or null')
    if baseline.keys() != comparison.keys():
        raise ValueError('fragment identity sets differ; reconcile inputs before comparing')
    transitions = {key: [] for key in ('00', '01', '10', '11')}
    abstentions = []
    for key in sorted(baseline):
        a, b = baseline[key], comparison[key]
        if a is None or b is None:
            abstentions.append({'fragment': key, 'baseline': a, 'comparison': b})
        else:
            transitions[f'{int(a)}{int(b)}'].append(key)
    n = {key: len(ids) for key, ids in transitions.items()}
    return {'identity_count': len(baseline), 'paired_denominator': sum(n.values()),
            'counts': n, 'net_change': n['01'] - n['10'], 'turnover': n['01'] + n['10'],
            'transitions': transitions, 'not_evaluable': abstentions}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('baseline', type=Path)
    parser.add_argument('comparison', type=Path)
    args = parser.parse_args()
    try:
        result = audit(*(json.loads(p.read_text(encoding='utf-8'), object_pairs_hook=unique_object)
                         for p in (args.baseline, args.comparison)))
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
