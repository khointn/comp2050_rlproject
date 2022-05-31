# analysis.py
# -----------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    answerDiscount = 0.9
    answerNoise = 0.0

    return answerDiscount, answerNoise

def question3a():
    # Strategy: low discount, no noise, survival penalty
    # => the further the reward, the less attractive
    # => no randomness, no chance falling into the cliff
    # => being alive for long (avoiding the cliff) is not advantageous
    answerDiscount = 0.2
    answerNoise = 0.0
    answerLivingReward = -1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3b():
    # Strategy: low discount, some noise, small survival reward
    # => the further the reward, the less attractive
    # => some randomness, chance falling into the cliff, hence avoid
    # => being alive is advantageous, but not too much
    answerDiscount = 0.2
    answerNoise = 0.2
    answerLivingReward = 0.5
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3c():
    # Strategy: high discount, no noise, survival penalty
    # => further reward are still attractive
    # => no randomness, no chance falling into the cliff
    # => being alive for long (avoiding the cliff) is not advantageous
    answerDiscount = 0.9
    answerNoise = 0.0
    answerLivingReward = -1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3d():
    # Strategy: high discount, noise, survival reward
    # => further reward are still attractive
    # => randomness, chance falling into the cliff, hence avoid
    # => being alive for long is advantageous
    answerDiscount = 0.8
    answerNoise = 0.4
    answerLivingReward = 1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3e():
    # Strategy: no discount, noise, survival reward
    # => reward are not attractive
    # => full randomness
    # => being alive for long is advantageous
    answerDiscount = 0
    answerNoise = 1
    answerLivingReward = 1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question8():
    # Q-learning needs high iterations
    return 'NOT POSSIBLE'
    # answerEpsilon = None
    # answerLearningRate = None
    # return answerEpsilon, answerLearningRate
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    print('Answers to analysis questions:')
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print('  Question %s:\t%s' % (q, str(response)))
