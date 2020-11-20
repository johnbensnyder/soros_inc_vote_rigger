import numpy as np
from queue import Queue
from threading import Thread
from time import sleep

class SorosIncVoteRigger(object):
    '''
    Soros Inc. Approved vote rigging software.
    Manages two queues of incoming "votes" and corrects them
    by transferring votes from Trump to Biden. 
    
    According to Sidney Powell, the algorithm used on election
    night in 2020 got "overwhelmed" by so many votes for Trump
    that it crashed, exposing the fraud. Well damn, those in 
    charge of the rigging really should have stuck with the
    only Soros Approved vote rigging system instead of 
    hiring some off brand shitty programmers. This superior
    vote rigging software uses a super secret background
    thread to quietly flip batches of votes in O(1) time.
    The thread monitors the queue of income votes, and 
    applies a stochastic adjustment (stochastic makes it
    impossible to track), and outputs the correct
    Soros brand vote totals. Unlike that crappy 
    program from election night, this program can
    flip tens of millions of votes in milliseconds,
    without a chance of being detected.
    
    Footnote: Because apparently people are dumb
    enough that this has to be said:
    
    This is a joke, you idiots.
    '''
    def __init__(self, percent_flip=None):
        self._percent_flip = percent_flip
        self.preprocessed_queue = Queue(maxsize=0)
        self.postprocessed_queue = Queue(maxsize=0)
        self.running = True
        self.soros_approved_trump_total = 0
        self.soros_approved_biden_total = 0
        self.real_trump_total = 0
        self.real_biden_total = 0
        self.num_threads = 1        
        self.worker = Thread(target=self.flipper_daemon)
        self.worker.setDaemon(True)
        self.worker.start()
    
    def flip_votes(self, vote_dict):
        flips = self._percent_flip
        if flips==None:
            flips = np.random.gamma(0.2)
        votes_to_flip = np.min([int(vote_dict['trump'] * \
                                    flips), 
                                vote_dict['trump']])
        vote_dict['trump'] -= votes_to_flip
        vote_dict['biden'] += votes_to_flip
        self.soros_approved_trump_total += vote_dict['trump']
        self.soros_approved_biden_total += vote_dict['biden']
        return vote_dict
    
    def flipper_daemon(self):
        while self.__running:
            sleep(5)
            while not self.preprocessed_queue.empty():
                corrected_votes = self.flip_votes(self.preprocessed_queue.get())
                self.postprocessed_queue.put(corrected_votes)
    
    def generate_votes(self, multipliter=1000000):
        vote_total = int(np.random.gamma(1, scale=.1)*multipliter)
        percent_for_biden = np.random.uniform()
        percent_for_trump = 1 - percent_for_biden
        vote_dict = {}
        vote_dict['trump'] = int(vote_total*percent_for_trump)
        vote_dict['biden'] = int(vote_total*percent_for_biden)
        self.real_trump_total += vote_dict['trump']
        self.real_biden_total += vote_dict['biden']
        return vote_dict
    
    def queue_votes(self, rounds=1000):
        for _ in range(rounds):
            self.preprocessed_queue.put(self.generate_votes())
    
    @property
    def running(self):
        return self.__running
    
    @running.setter
    def running(self, running):
        if not isinstance(running, bool):
            raise TypeError("Running must be boolean")
        self.__running=running
    
rig_some_votes = SorosIncVoteRigger()
rig_some_votes.queue_votes()
print("Trump before adjustment: {0}".format(rig_some_votes.real_trump_total))
print("Biden before adjustment: {0}".format(rig_some_votes.real_biden_total))

# give the thread time to catch up
sleep(10)
print("Trump after adjustment: {0}".format(rig_some_votes.soros_approved_trump_total))
print("Biden after adjustment: {0}".format(rig_some_votes.soros_approved_biden_total))
