import pytest
from turbo_invention.compliance.safe import five_safes_gate

def test_blocks_when_any_unflagged():
    with pytest.raises(PermissionError):
        five_safes_gate(people=True, project=True, setting=True,
                        data=False, outputs=True)

def test_passes_when_all_flagged():
    five_safes_gate(people=True, project=True, setting=True,
                    data=True, outputs=True)
