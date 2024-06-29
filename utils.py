import requests, bs4, enum, sys

class Answers(enum.Enum):
    ANS: str = "ANS"
    CE : str = "CE"
    UD : str = "UD"
    US : str = "US"

class CPPQuiz:
    def __init__(self, q_id: int = None, answer: str = None) -> None:
        self.q_id = q_id
        self.answer = answer
    
    def is_valid(this, response: requests.Response):
        return response.status_code == 200

    def lookfor_question(this, q_id: int = None):
        if q_id is None:
            q_id = this.q_id
        assert (q_id), "Question ID must be filled."
        r = requests.get(f"https://cppquiz.org/quiz/question/{q_id}")
        if this.is_valid(r):
            parser = bs4.BeautifulSoup(r.content, "html.parser")
            code = parser.select_one("pre").select_one("code").text
            return code
        return -1

    def validate_answer_for_question(this, q_id: int = None, answer: str = None):
        if q_id is None:
            q_id   =  this.q_id
        if answer is None:
            answer =  this.answer
        assert (q_id and answer), "Question ID and Answer must be filled."
        r = requests.get(f"https://cppquiz.org/quiz/question/{q_id}?result=OK&answer={answer}&did_answer=Answer")
        if this.is_valid(r):
            parser = bs4.BeautifulSoup(r.content, "html.parser")
            is_correct = parser.select_one("div#correct")
            if is_correct:
                return is_correct.text
            return bool(is_correct)
        return False
    
    def play(this, q_id: int, qs: str):
        print(f"Question - #{q_id}\n\n{qs}\n")
        print("* CE: Compilation Error\n* UD: Undefined Behaviour\n* US: Unspecified Behaviour\nThere is no error and answer will be: .....\n")

        answer = input("What is the answer?")
        result = False
        while (not result):
            result = this.validate_answer_for_question(q_id, answer)
            if result:
                break
            else:
                print("You lost! You can try again...")
                answer = input("What is the answer?")
        print("You won!")
        print(result)
        ask_for_another = input("Wanna new another question (Y/n)?").lower()
        if "y" in ask_for_another:
            this.play(*this.get_random_question())
    
    def get_random_question(this):
        r = requests.get(f"https://cppquiz.org/quiz/random")
        q_id = r.url.split("/")[-1]
        print("new question: ", q_id)
        return (q_id, this.lookfor_question(q_id))
