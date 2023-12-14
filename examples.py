from utils import CPPQuiz

if __name__ == "__main__":
    base = CPPQuiz()
    commands = sys.argv[1:]
    assert ("--rand" not in commands or "--id" not in commands), "rand and id keyword argument cannot use same time."
    if "--rand" in commands:
        q_id, qs = base.get_random_question()
    elif "--id" in commands:
        q_id = commands[commands.index("--id")+1]
        qs = base.lookfor_question(q_id)
    else:
        print("No args found!")
        quit()
    base.play(q_id, qs)
