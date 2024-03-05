# The purpose of qasmevalutils.py is to provide utilities functions to help to evaluate model completions against human completions using Sequence manager.
from difflib import SequenceMatcher
import json

def sm_matching_test(response_r, response_e, matching_threshold=0.6, debug=False):
    sequence_matcher = SequenceMatcher(None, response_r, response_e)
    matching_ratio = sequence_matcher.ratio()
    reason = f"Using a threshold value of : {matching_threshold} vs {matching_ratio}"
    test_result = {
        "test_id":1,
        "test":"sequence_matcher_similarity",
        "result":int(matching_ratio >= matching_threshold),
        "reason":reason
    }
    if debug: print(f"sm_matching_test : test_result : {test_result}")
    return test_result
