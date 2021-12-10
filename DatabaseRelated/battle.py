class Battle:
    def __init__(self,p1, p2, gained_rank = 0, lost_rank = 0, dispute=False, p1Win = False):
        self.p1= p1
        self.p2 = p2
        self.gained_rank = gained_rank
        self.lost_rank= lost_rank  
        self.dispute = dispute
        self.p1Win = p1Win
        
    #probably wont need these because of looking in server.
    def get_p1(self):
        return self.p1
    def set_p1(self,p1):
        self.p1 = p1
    #probably wont need these
    def get_p2(self):
        return self.p2
    def set_p1(self,p2):
        self.p2 = p2

    def get_gained_rank(self):
        return self.gained_rank
    def set_gained_rank(self,gained_rank):
        self.gained_rank = gained_rank

    def get_lost_rank(self):
        return self.get_lost_rank
    def set_lost_rank(self,lost_rank):
        self.lost_rank= lost_rank

    def set_dispute(self,dispute):
        self.dispute = dispute

    def set_p1Win(self,p1Win):
        self.p1Win = p1Win    

            
