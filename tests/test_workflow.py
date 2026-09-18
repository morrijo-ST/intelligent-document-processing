from pathlib import Path
import numpy as np
from streamlit.testing.v1 import AppTest

APP=Path(__file__).resolve().parents[1]/'app.py'
def app():
    at=AppTest.from_file(str(APP),default_timeout=30).run()
    assert not at.exception
    return at

def test_threshold_preserves_duplicate_blocks_and_releases_eligible_matches():
    at=app()
    for threshold in [.98,.70]:
        at.slider[0].set_value(threshold).run()
        assert not at.exception
        register=at.dataframe[-1].value
        assert (register.loc[register.duplicate,'match_status']=='Duplicate').all()
        eligible=(~register.duplicate)&(register.confidence>=threshold)&(register.variance.abs()<=np.maximum(25,register.po_amount*.02))
        assert (register.match_status.eq('Matched')==eligible).all()
