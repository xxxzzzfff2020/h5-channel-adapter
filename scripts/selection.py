#!/usr/bin/env python3
"""Persist explicit adaptation scope. This helper never edits a game or calls a platform."""
import argparse
import json
from pathlib import Path
import sys

CATALOG = json.loads((Path(__file__).resolve().parents[1] / 'assets/capabilities.json').read_text(encoding='utf-8'))
MATERIALS = ('images_copy', 'images_copy_video', 'projects_only')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def choices(value, allowed, name, nonempty=False):
    require(isinstance(value, list) and all(isinstance(x, str) for x in value), name + ' must be an explicit list')
    require(len(set(value)) == len(value), name + ' contains duplicates')
    require(not nonempty or bool(value), name + ' requires at least one selection')
    require(set(value) <= set(allowed), name + ' contains an unknown choice')
    return value


def check_source(source):
    require(isinstance(source, dict), 'source is required')
    require(source.get('kind') in CATALOG['source_kinds'], 'source.kind must be a supported H5 source type; Maker Lua is not H5')
    require(isinstance(source.get('path'), str) and bool(source['path'].strip()), 'source.path is required')
    require(isinstance(source.get('inspection'), str) and bool(source['inspection'].strip()), 'Record source inspection: entry/build and existing platform hooks')
    require(isinstance(source.get('existing_integrations'), list) and all(isinstance(x, str) for x in source['existing_integrations']), 'existing_integrations must be an inspected list (empty is allowed)')


def compile_answers(answers):
    require(isinstance(answers, dict), 'answers must be an object')
    require(answers.get('confirmed') is True, 'No confirmed user answer; no scope created')
    check_source(answers.get('source'))
    targets = choices(answers.get('targets'), CATALOG['targets'], 'targets', True)
    feature_answers = answers.get('features')
    material_answers = answers.get('materials')
    require(isinstance(feature_answers, dict) and set(feature_answers) == set(targets), 'Explicit feature list required for every selected target, and only selected targets')
    require(isinstance(material_answers, dict) and set(material_answers) == set(targets), 'Explicit material choice required for every selected target, and only selected targets')
    logic = choices(answers.get('game_logic'), CATALOG['game_logic_options'], 'game_logic')
    channels = {}
    for target, spec in CATALOG['targets'].items():
        selected = target in targets
        picked = choices(feature_answers[target], spec['features'], target + '.features') if selected else []
        material = material_answers.get(target)
        require(not selected or material in MATERIALS, 'Unknown material scope for ' + target)
        channels[target] = {
            'selected': selected, 'materials': material,
            'features': {f: {'selected': f in picked, 'status': 'pending_verification' if f in picked else 'not_selected', 'evidence': []} for f in spec['features']}}
    result = {'schema_version': 1, 'confirmed': True, 'source': answers['source'], 'targets': targets, 'channels': channels, 'game_logic': logic}
    validate(result)
    return result


def validate(config):
    require(isinstance(config, dict) and config.get('schema_version') == 1 and config.get('confirmed') is True, 'Expected confirmed scope schema 1')
    check_source(config.get('source'))
    targets = choices(config.get('targets'), CATALOG['targets'], 'targets', True)
    choices(config.get('game_logic'), CATALOG['game_logic_options'], 'game_logic')
    channels = config.get('channels')
    require(isinstance(channels, dict) and set(channels) == set(CATALOG['targets']), 'Scope must record all catalog targets, including not selected')
    for target, spec in CATALOG['targets'].items():
        entry = channels[target]
        require(isinstance(entry, dict), 'Invalid channel record')
        selected = target in targets
        require(entry.get('selected') is selected, 'Target selection mismatch: ' + target)
        require(entry.get('materials') in MATERIALS if selected else entry.get('materials') is None, 'Material selection mismatch: ' + target)
        features = entry.get('features')
        require(isinstance(features, dict) and set(features) == set(spec['features']), 'Feature catalog mismatch: ' + target)
        for feature, state in features.items():
            require(isinstance(state, dict) and type(state.get('selected')) is bool, 'Invalid feature selection')
            require(state.get('status') in CATALOG['statuses'], 'Invalid feature status')
            require(isinstance(state.get('evidence'), list) and all(isinstance(x, str) and x.strip() for x in state['evidence']), 'Evidence must be a list of nonempty references')
            if not selected or not state['selected']:
                require(state['selected'] is False and state['status'] == 'not_selected', 'Unselected feature cannot be activated: ' + target + '/' + feature)
            else:
                require(state['status'] != 'not_selected', 'Selected feature cannot have not_selected status')
                if state['status'] in ('configured', 'unsupported'):
                    require(bool(state['evidence']), 'Configured/unsupported status needs current evidence')
    return config


def plan(config):
    validate(config)
    return {'source': config['source'], 'game_logic': config['game_logic'], 'targets': [
        {'target': target, 'materials': config['channels'][target]['materials'],
         'processing': {'video': config['channels'][target]['materials'] == 'images_copy_video'},
         'features': {name: state for name, state in config['channels'][target]['features'].items() if state['selected']},
         'next': {name: {'pending_verification': 'verify_selected_capability', 'unsupported': 'report_gap_no_integration', 'configured': 'validate_target_implementation'}[state['status']] for name, state in config['channels'][target]['features'].items() if state['selected']}}
        for target in config['targets']]}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('command', choices=('create', 'validate', 'plan'))
    ap.add_argument('input', type=Path, help='Answers JSON for create; saved selection JSON otherwise')
    ap.add_argument('--output', type=Path, help='New saved selection file (create only); existing files are never overwritten')
    args = ap.parse_args()
    try:
        value = json.loads(args.input.read_text(encoding='utf-8'))
        if args.command == 'create':
            result = compile_answers(value)
            require(args.output is not None, 'create requires --output')
            # Validate everything before touching the destination. Exclusive mode protects prior scope.
            with args.output.open('x', encoding='utf-8') as stream:
                stream.write(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        else:
            require(args.output is None, '--output is only valid for create')
            result = plan(value) if args.command == 'plan' else validate(value)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError, TypeError) as exc:
        print('Selection error: ' + str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
