"""Synthetic scope, resume and TapTap helper regressions; no accounts or game data."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from selection import CATALOG, compile_answers, validate, plan
from verify_game_package import inspect
from check_package_budget import check
from verify_materials import validate as materials


def exercise(base):
    results = []
    answers = {'confirmed': True, 'source': {'kind': 'generic_h5', 'path': str(base / 'source'), 'inspection': 'Synthetic HTML entry; no platform hooks', 'existing_integrations': []}, 'targets': ['taptap', '4399'], 'features': {'taptap': ['local_save', 'cloud_save'], '4399': ['ads']}, 'materials': {'taptap': 'projects_only', '4399': 'images_copy'}, 'game_logic': []}
    config = compile_answers(answers)
    saved = base / 'scope.json'; saved.write_text(json.dumps(config), encoding='utf-8')
    resumed = plan(json.loads(saved.read_text(encoding='utf-8')))
    assert [x['target'] for x in resumed['targets']] == ['taptap', '4399']
    assert set(resumed['targets'][0]['features']) == {'local_save', 'cloud_save'}
    assert set(resumed['targets'][1]['features']) == {'ads'}
    assert not any(x['processing']['video'] for x in resumed['targets'])
    results.append('selection-roundtrip-targets-and-per-target-features')
    for target in set(CATALOG['targets']) - set(answers['targets']):
        assert all(s['status'] == 'not_selected' for s in config['channels'][target]['features'].values())
    results.append('unselected-platforms-and-features-inactive')

    for source in CATALOG['source_kinds']:
        a=copy.deepcopy(answers); a['source']['kind']=source
        assert compile_answers(a)['source']['kind'] == source
    results.append('all-three-source-kinds')
    a=copy.deepcopy(answers); a.update(targets=['taptap'], features={'taptap': []}, materials={'taptap': 'images_copy_video'})
    a['source']['kind']='taptap_h5'
    output=plan(compile_answers(a)); assert len(output['targets'])==1 and output['targets'][0]['features']=={} and output['targets'][0]['processing']['video']
    results.append('taptap-same-channel-empty-features-explicit-video')

    mutations=[('no-confirmation', lambda a:a.pop('confirmed')), ('false-confirmation',lambda a:a.update(confirmed=False)), ('empty-targets',lambda a:a.update(targets=[])), ('duplicate-targets',lambda a:a.update(targets=['taptap','taptap'])), ('unknown-target',lambda a:a.update(targets=['invented'])), ('maker-not-h5',lambda a:a['source'].update(kind='maker_lua')), ('missing-inspection',lambda a:a['source'].pop('inspection')), ('missing-feature-answer',lambda a:a['features'].pop('4399')), ('unselected-target-answer',lambda a:a['features'].update(xingxia=['ads'])), ('unknown-feature',lambda a:a['features'].update(taptap=['invented'])), ('duplicate-feature',lambda a:a['features'].update(taptap=['ads','ads'])), ('missing-material-answer',lambda a:a['materials'].pop('4399')), ('unknown-material',lambda a:a['materials'].update(taptap='all')), ('missing-game-logic-answer',lambda a:a.pop('game_logic'))]
    for name, mutate in mutations:
        a=copy.deepcopy(answers);mutate(a)
        try: compile_answers(a)
        except ValueError: pass
        else: raise AssertionError(name+' should fail')
        results.append('selection-rejects-'+name)

    for channel,feature in [('xingxia','ads'),('taptap','ads')]:
        bad=copy.deepcopy(config);bad['channels'][channel]['features'][feature].update(selected=True,status='configured',evidence=['synthetic'])
        if channel=='taptap': # explicit tampering is new scope, never an implicit status update
            bad['channels'][channel]['features'][feature]['selected']=False
        try: validate(bad)
        except ValueError: pass
        else: raise AssertionError('unselected activation')
    results.append('resume-rejects-status-on-unselected-feature-or-target')
    feature=config['channels']['taptap']['features']['cloud_save']
    for status in ['configured','unsupported']:
        feature.update(status=status,evidence=[])
        try: validate(config)
        except ValueError: pass
        else: raise AssertionError('missing evidence')
        feature['evidence']=['Synthetic dated verification; not real SDK evidence']
        output=plan(config)
        assert output['targets'][0]['next']['cloud_save'] == ('validate_target_implementation' if status=='configured' else 'report_gap_no_integration')
    results.append('resume-status-needs-evidence-and-unsupported-never-integrates')

    script=Path(__file__).resolve().parents[1]/'scripts/selection.py'
    a=base/'answers.json'; dest=base/'created.json'; a.write_text(json.dumps(answers))
    def run(expected):
        proc=subprocess.run([sys.executable,str(script),'create',str(a),'--output',str(dest)],capture_output=True,text=True)
        assert proc.returncode==expected, proc.stderr
    bad=copy.deepcopy(answers);bad.pop('confirmed');a.write_text(json.dumps(bad));run(2);assert not dest.exists()
    results.append('no-answer-cli-does-not-write')
    a.write_text(json.dumps(answers));run(0);before=dest.read_bytes();run(2);assert dest.read_bytes()==before
    results.append('cli-protects-existing-selection')
    proc=subprocess.run([sys.executable,str(script),'plan',str(dest)],capture_output=True,text=True)
    assert proc.returncode==0 and json.loads(proc.stdout)['targets'][0]['target']=='taptap'
    results.append('cli-resumes-persisted-selection')

    package=base/'taptap.zip'
    with zipfile.ZipFile(package,'w') as z:z.writestr('game/index.html','<html><body>Synthetic H5</body></html>')
    assert inspect(package,'taptap')['status']=='pass'
    results.append('taptap-static-package')
    budget=check(package,['taptap'],Path(__file__).resolve().parents[1]/'assets/package-rules.json','candidate')
    assert budget['overall_status']=='within_known_limits' and budget['checks'][0]['max_bytes']==300000000
    assert 'manual upload' in budget['checks'][0]['basis']
    results.append('taptap-manual-zip-budget-300-decimal-mb')
    with zipfile.ZipFile(package,'w') as z:z.writestr('game/index.html','<script src="https://cdn.233xyx.com/h5ad/metah5ad_v1.min.js"></script>')
    assert any('wrong-channel' in e.lower() for e in inspect(package,'taptap')['errors'])
    results.append('taptap-rejects-known-other-channel-sdk')
    manifest=base/'taptap-materials.json';manifest.write_text(json.dumps({'channel':'taptap','game':'Synthetic','source_version':'fixture','processing':{'video':False},'files':[]}))
    report=materials(manifest, Path(__file__).resolve().parents[1]/'assets/material-rules.json')
    assert report['warnings'] and not report['errors'] and not report['profile_complete']
    data=json.loads(manifest.read_text());data['processing']['video']=True;manifest.write_text(json.dumps(data))
    report=materials(manifest, Path(__file__).resolve().parents[1]/'assets/material-rules.json')
    assert report['technical_status']=='pass' and not report['profile_complete']
    results.append('taptap-material-unknown-rules-remain-visible')
    return results
