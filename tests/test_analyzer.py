import analyzer.analyze
import os
import json
import pytest

test_dir = os.path.dirname(__file__)
rel_path = "fixtures/input.json"
abs_file_path = os.path.join(test_dir, rel_path)


test_json = open(abs_file_path).read()

def test_analyze():
    test_data = json.loads(test_json)
    res = analyzer.analyze.analyze(test_data)
    assert len(res['refuelStops']) == 1
    assert len(res['breaks']) == 1
    assert res['departure'] == 'Stuttgart'
    assert res['destination'] ==  'Bad Salzungen'
    assert res['consumption'] == pytest.approx(4.5, abs=0.1)
    assert res['vin'] == 'WDD1671591Z000999'
