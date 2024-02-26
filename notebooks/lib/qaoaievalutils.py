# The purpose of qaoaievalutils.py is to provide utilities functions to help to evaluate model completions against human completions using standard Azure OpenAI API.
import json
import aoaiutils

EVAL_ROBOT_VS_HUMAN_PROMPT = """<|im_start|>user
    Compare the robot response versus human response. The robot response is delimited by ###ROBOT### and 
    the human response is delimited by ###HUMAN###.
    Answer the next questions:
    Question-1 : Is the robot's response correct?
    Question-2 : Is the robot's response similar to the human answer?
    For your responses follow the next format:
    Question-1--Correctness--YES or NO--Summarize your arguments in 10 words
    Question-2--Similarity--YES or NO--Summarize your arguments in 10 words
    
    ###ROBOT###
    {robot_response}
    ###ROBOT###
    
    ###HUMAN###
    {human_response}
    ###HUMAN###
    <|im_end|><|im_start|>assistant"""


EVAL_QUERY_ROBOT_VS_HUMAN_PROMPT = """<|im_start|>user
    Evaluate the robot response against the query.
    Evaluate the human response against the query.
    Compare the robot response versus human response.
    The query is delimited by ###QUERY###.
    The robot response is delimited by ###ROBOT###. 
    The human response is delimited by ###HUMAN###.
    Answer the next questions:
    Question-1 : Is the robot's response similar to the human answer?
    Question-2 : Is the robot's response correct?
    Question-3 : Is the human's response correct?
    For your responses follow the next format:
    Question-1--Similarity--YES or NO--Summarize your arguments in 10 words
    Question-2--Robot Correctness--YES or NO--Summarize your arguments in 10 words
    Question-3--Human Correctness--YES or NO--Summarize your arguments in 10 words

    ###QUERY###
    {query}
    ###QUERY###

    ###ROBOT###
    {robot_response}
    ###ROBOT###
    
    ###HUMAN###
    {human_response}
    ###HUMAN###
    <|im_end|><|im_start|>assistant"""

EVAL_QUERY_BETTER_RESPONSE = """<|im_start|>user
    Evaluate the response A against the query.
    Evaluate the response B against the query.
    Compare response A versus response B.
    The query is delimited by ###QUERY###.
    The response A is delimited by ###RESPONSE_A###. 
    The response B is delimited by ###RESPONSE_B###.
    Answer the next questions:
    Question-1 : Is the response A similar to response B?
    Question-2 : Is the response A correct?
    Question-3 : Is the response B correct?
    Question-4 : Which response is better?
    For the next questions, on a scale of 1 to 10, where 1 is the lowest score and 10 the highest, score simplicity 
    and relevant information.
    Question-5 : What would be the score for response A?
    Question-6 : What would be the score for response B?
    For your responses follow the next format:
    Question-1--Similarity--YES or NO--Summarize your arguments in 10 words
    Question-2--Response A Correctness--YES or NO--Summarize your arguments in 10 words
    Question-3--Response B Correctness--YES or NO--Summarize your arguments in 10 words
    Question-4--Better response--A or B--Summarize your arguments in 10 words
    Question-5--Score A --Number between 1 and 10--Summarize your arguments in 10 words
    Question-6--Score B --Number between 1 and 10--Summarize your arguments in 10 words

    ###QUERY###
    {query}
    ###QUERY###

    ###RESPONSE_A###
    {response_a}
    ###RESPONSE_A###
    
    ###RESPONSE_B###
    {response_b}
    ###RESPONSE_B###
    <|im_end|><|im_start|>assistant"""

def transform_open_ai_compare_to_json(input_string, debug=False):
    data = []
    if debug: print(f"transform_open_ai_compare_to_json : input to process : {input_string}")
    parts = input_string.replace("\n", "").replace("\r", "").split("Question-")
    if debug: print(f"parts : {parts}")
    for i, part in enumerate(parts, start=1):
        if part:
            info = part.split("--")
            if debug: print(f"transform_open_ai_compare_to_json : i: {i} part: {part} info: {info}")
            test_id = info[0]
            test = info[1]
            if info[2] == "YES":
                result = 1
            elif info[2] == "NO":
                result = 0
            else:
                result = info[2]
            reason = info[3]
            item = {
                "test_id": test_id,
                "test": test,
                "result": result,
                "reason": reason
            }
            if debug: print(f"transform_open_ai_compare_to_json : Item to add : {item}")
            data.append(item)
    if debug: print(f"transform_open_ai_compare_to_json : data to json : {data}")
    return json.dumps(data, indent=2)

def evaluate_robot_vs_human_response(robot_answer, human_answer, debug=False):
    prompt = EVAL_ROBOT_VS_HUMAN_PROMPT.format(robot_response=robot_answer, human_response=human_answer)
    if debug: print(f"evaluate_robot_vs_human_response : prompt : {prompt}")
    
    completion = aoaiutils.get_completion(input_prompt=prompt,debug=debug)
    result_as_json = transform_open_ai_compare_to_json(input_string=completion,debug=debug)
    if debug: print(f"evaluate_robot_vs_human_response : result : {result_as_json}") 
    return result_as_json
    
def evaluate_query_robot_vs_human_response(user_query, robot_answer, human_answer, debug=False):
    prompt = EVAL_QUERY_ROBOT_VS_HUMAN_PROMPT.format(robot_response=robot_answer, human_response=human_answer,query=user_query)
    if debug: print(f"evaluate_query_robot_vs_human_response : prompt : {prompt}")
    
    completion = aoaiutils.get_completion(input_prompt=prompt,debug=debug)
    result_as_json = transform_open_ai_compare_to_json(input_string=completion,debug=debug)
    if debug: print(f"evaluate_query_robot_vs_human_response : result : {result_as_json}") 
    return result_as_json

def evaluate_query_better_response(user_query, response_a, response_b, debug=False):
    prompt = EVAL_QUERY_BETTER_RESPONSE.format(response_a=response_a, response_b=response_b, query=user_query)
    if debug: print(f"evaluate_query_better_response : prompt : {prompt}")
    
    completion = aoaiutils.get_completion(input_prompt=prompt,debug=debug)
    result_as_json = transform_open_ai_compare_to_json(input_string=completion,debug=debug)
    if debug: print(f"evaluate_query_better_response : result : {result_as_json}") 
    return result_as_json
