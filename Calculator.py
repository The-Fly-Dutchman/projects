import random, operator, json

class Calculator:

    ops = {'+':operator.add,
           '-':operator.sub,
           '*':operator.mul,
           '/':operator.truediv}

    num_points = 0
    streak = 0
    upper_bound = 10
    dummy_count = 0

    @classmethod
    def load_previous_score(cls):
        with open("score.json", "r") as file:
            data = json.load(file)
            cls.num_points = data['points']
            cls.streak = data['streak']
            cls.upper_bound = data['upper_bound']

    @classmethod
    def random_generator(cls):
        op = random.choice(list(cls.ops.keys()))
        r1 = random.randint(1, cls.upper_bound)
        r2 = random.randint(1, cls.upper_bound)
        if op == '/':
          while r2 % r1 != 0:
            r1 = random.randint(1, cls.upper_bound)
            r2 = random.randint(1, cls.upper_bound)
        return r1, op, r2

    @classmethod
    def compile_question(cls):
        r1, op, r2 = cls.random_generator()
        if r2 > r1 and op in ['/', '-']:
            a = '{} {} {}'.format(r2, op, r1)
            true_answer = int(eval(a))
            question = 'What is {} {} {}?'.format(r2, op, r1)
            return question, true_answer
        else:
            a = '{} {} {}'.format(r1, op, r2)
            true_answer = int(eval(a))
            question = 'What is {} {} {}?'.format(r1, op, r2)
            return question, true_answer

    @classmethod
    def master_compiler(cls):
        if cls.dummy_count == 0:
            cls.load_previous_score()
        question, true_answer = cls.compile_question()
        print(question)
        given_answer = input('Input your answer here: ')
        try:
            int(given_answer)
        except ValueError:
            print('Invalid input, that is not a number')
            given_answer = input('Input your answer here: ')
        given_answer = int(given_answer)
        while given_answer != true_answer:
            cls.num_points = 0
            cls.streak = 0
            print('Try again. You have {} points and have answered {} question(s) successfully in a row.'.format(cls.num_points, cls.streak))
            print(question)
            given_answer = int(input('Input your answer here: '))
        cls.num_points += (1 + cls.streak // 5)
        cls.streak += 1
        if cls.streak % 5 == 0:
            cls.num_points += 10
        print("You're correct! You have {} points and have answered {} question(s) successfully in a row.".format(cls.num_points, cls.streak))
        if (cls.streak % 5) == 0:
            cls.upper_bound += 10
        cont = input('Continue? (y/n) ')
        if cont == 'y':
            cls.dummy_count = 1
            cls.master_compiler()
        elif cont == 'n':
            save_score = dict()
            save_score["points"] = cls.num_points
            save_score["streak"] = cls.streak
            save_score["upper_bound"] = cls.upper_bound
            with open("score.json", "w") as file:
                json.dump(save_score, file)
            file.close()
            cls.dummy_count = 0

Calculator.master_compiler()



