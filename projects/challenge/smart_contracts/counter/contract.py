# pyright: reportMissingModuleSource=false
from algopy import ARC4Contract, LocalState, GlobalState, UInt64, Txn, arc4, Global, gtxn, Account


class Counter(ARC4Contract):
    def __init__(self) -> None:
        self.counters = GlobalState(UInt64)     # counters key, UInt64 value
        self.counters.value = UInt64(0)         # init counters value
    
    #count: LocalState[UInt64] 
    #counters: GlobalState[UInt64]

    @arc4.baremethod(allow_actions=["OptIn"])
    def opt_in(self) -> None:
        self.count = LocalState(UInt64)         # count key, UInt64 value
        self.count[Txn.sender] = UInt64(0)      # init count value on opt_in
        self.counters.value += 1

    @arc4.abimethod()
    def increment(self) -> arc4.UInt64:
        assert Txn.sender.is_opted_in(
            Global.current_application_id
        ), "Sender must opt-in to the contract"
        self.count[Txn.sender] += 1
        return arc4.UInt64(self.count[Txn.sender])
