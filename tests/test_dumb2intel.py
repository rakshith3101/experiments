from dumb2intel.engine import generate_text

def test_generate_text():
    response = generate_text("Test prompt")
    assert isinstance(response, str)
    assert len(response) > 0
    