import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python'))

from checker import (
    check_length,
    check_character_variety,
    check_common_password,
    check_repeated_chars,
    calculate_strength
)
def test_length_too_short():
    result = check_length("abc")
    assert result["pass"] is False
def test_length_exact_minimum():
    result = check_length("abcdefgh")
    assert result["pass"] is True
def test_length_good():
    result = check_length("MyPassword12")
    assert result["pass"] is True
def test_length_excellent():
    result = check_length("ThisIsAVeryLongPassword99!")
    assert result["pass"] is True
    assert result["length"] >= 16
def test_variety_all_present():
    result = check_character_variety("Abc1@xyz")
    assert result["uppercase"] is True
    assert result["lowercase"] is True
    assert result["digit"] is True
    assert result["symbol"] is True
    assert result["variety_score"] == 4
def test_variety_only_lowercase():
    result = check_character_variety("abcdefgh")
    assert result["uppercase"] is False
    assert result["lowercase"] is True
    assert result["digit"] is False
    assert result["symbol"] is False
    assert result["variety_score"] == 1
def test_variety_numbers_and_upper():
    result = check_character_variety("HELLO123")
    assert result["uppercase"] is True
    assert result["digit"] is True
    assert result["lowercase"] is False
    assert result["variety_score"] == 2
def test_common_password_detected():
    assert check_common_password("password") is True
    assert check_common_password("123456") is True
    assert check_common_password("letmein") is True
def test_common_password_case_insensitive():
    assert check_common_password("PASSWORD") is True
    assert check_common_password("Password") is True
def test_non_common_password():
    assert check_common_password("Tr0ub4dor&3") is False
    assert check_common_password("Xk9#mPqL!vR2") is False
def test_repeated_chars_detected():
    assert check_repeated_chars("aaabcde") is True
    assert check_repeated_chars("abc111xyz") is True
    assert check_repeated_chars("hello!!!") is True
def test_no_repeated_chars():
    assert check_repeated_chars("abcABC123!") is False
    assert check_repeated_chars("aabb") is False
def test_weak_common_password():
    result = calculate_strength("password")
    assert result["strength"] == "WEAK"
def test_weak_too_short():
    result = calculate_strength("Hi1!")
    assert result["strength"] == "WEAK"
def test_weak_simple():
    result = calculate_strength("abcdefgh")
    assert result["strength"] == "WEAK"
def test_medium_password():
    result = calculate_strength("Admin1234")
    assert result["strength"] in ("WEAK", "MEDIUM")
def test_strong_password():
    result = calculate_strength("Tr0ub4dor&3!")
    assert result["strength"] == "STRONG"
def test_strong_long_password():
    result = calculate_strength("Cyber$ecurity2026!DecodeLabs")
    assert result["strength"] == "STRONG"
def test_empty_password():
    result = calculate_strength("")
    assert result["strength"] == "INVALID"
def test_feedback_not_empty():
    result = calculate_strength("weakpass")
    assert len(result["feedback"]) > 0
def test_score_non_negative():
    result = calculate_strength("aaa")
    assert result["score"] >= 0

if __name__ == "__main__":
    tests = [
        test_length_too_short,
        test_length_exact_minimum,
        test_length_good,
        test_length_excellent,
        test_variety_all_present,
        test_variety_only_lowercase,
        test_variety_numbers_and_upper,
        test_common_password_detected,
        test_common_password_case_insensitive,
        test_non_common_password,
        test_repeated_chars_detected,
        test_no_repeated_chars,
        test_weak_common_password,
        test_weak_too_short,
        test_weak_simple,
        test_medium_password,
        test_strong_password,
        test_strong_long_password,
        test_empty_password,
        test_feedback_not_empty,
        test_score_non_negative,
    ]

    passed = 0
    failed = 0

    print("\n  🧪  Running Tests — Password Strength Checker\n")
    print("  " + "—" * 40)

    for test_fn in tests:
        try:
            test_fn()
            print(f"  ✓  {test_fn.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  ✗  {test_fn.__name__}  ← FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗  {test_fn.__name__}  ← ERROR: {e}")
            failed += 1

    print("  " + "—" * 40)
    print(f"\n  Results: {passed} passed, {failed} failed\n")
