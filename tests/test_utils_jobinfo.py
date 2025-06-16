from utils.utils_jobinfo import basic_field_extraction


def test_basic_field_extraction_skills():
    text = "Proficiency in Python and machine learning libraries (e.g., scikit-learn, TensorFlow)."
    result = basic_field_extraction(text)
    assert (
        result["must_have_skills"]
        == "Python, machine learning libraries, scikit-learn, TensorFlow"
    )
