class POSIXThreadsObjectsPrinter(BasePrettyPrinter):
    """Pretty print a _POSIX_Threads_Objects."""
    
    def __init__(self, val):
        self.val = val

    def to_string(self):
        thread_id = self.val['thread_id']
        stack = self.val['stack']
        priority = self.val['priority']
        chain = self.val['chain']
        
        return (f"_POSIX_Threads_Objects(\n"
                f"    thread_id={thread_id},\n"
                f"    stack={stack},\n"
                f"    priority={priority},\n"
                f"    chain={chain}\n"
                f")")