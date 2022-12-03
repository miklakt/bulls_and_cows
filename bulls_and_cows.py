#%%
import itertools
import random

possible_results = []
for res in itertools.product([0,1,2,3,4], [0,1,2,3,4]):
    if res[0]+res[1]<5:
        possible_results.append(res)

all_numbers = ["".join(it) for it in itertools.permutations("0123456789", 4)]
random.shuffle(all_numbers)
#%%
def give_answer(secret_number : str, guess :str):
    bulls = 0
    cows = 0
    for i, digit in enumerate(guess):
        if digit in secret_number:
            if digit == secret_number[i]: bulls+=1
            else: cows+=1
    return bulls, cows

def check_if_secret_possible(candidate_number: str, known_number : str, n_bulls : str, n_cows : str):
    bulls, cows = give_answer(known_number, candidate_number)
    if (bulls==n_bulls) and (cows==n_cows):
        return True
    else:
        return False

def strike_out(candidate_list: list, known_number : str, n_bulls : str, n_cows : str):
    rest =[]
    stricked_out = 0
    for candidate in candidate_list:
        if check_if_secret_possible(candidate, known_number, n_bulls, n_cows):
            rest.append(candidate)
        else:
            stricked_out+=1
    return rest, stricked_out

def propose_next_guess(candidate_list: list):
    if len(candidate_list) == 1: return candidate_list[0]
    next_guess = all_numbers[0]
    maxmin_score = 0 #best of the worst results
    for number in all_numbers:
        min_score=1e5 #worst result
        for bulls, cows in possible_results:
            _, stricked_out = strike_out(candidate_list, number, bulls, cows)
            if stricked_out<min_score: min_score = stricked_out
        if min_score>maxmin_score:
            maxmin_score=min_score
            next_guess = number
            #print(number, maxmin_score)
    return next_guess
#%%
if __name__=="__main__":
    secret_number = random.choice(all_numbers)
    print(f"Secret number: {secret_number}")

    #debute
    candidates=all_numbers
    next_guess ="1234"
    tries = 1
    bulls, cows = give_answer(secret_number, next_guess)
    candidates,_ = strike_out(candidates, next_guess, bulls, cows)
    print(f"{tries}) {next_guess} {bulls} {cows}")

    next_guess ="5678"
    tries +=1
    bulls, cows = give_answer(secret_number, next_guess)
    candidates,_ = strike_out(candidates, next_guess, bulls, cows)
    print(f"{tries}) {next_guess} {bulls} {cows}")

    while True:
        next_guess = propose_next_guess(candidates)
        tries +=1
        bulls, cows = give_answer(secret_number, next_guess)
        candidates,_ = strike_out(candidates, next_guess, bulls, cows)
        print(f"{tries}) {next_guess} {bulls} {cows}")
        if bulls == 4: break

    print(f"You number is: {next_guess}")
