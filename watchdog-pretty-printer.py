import gdb

class RBTreeNodePrinter:
    """Print an RBTree_Node structure."""
    def __init__(self, val):
        self.val = val

    def to_string(self):
        return "RBTree_Node(left={}, right={}, parent={}, color={})".format(
            self.val['rbe_left'],
            self.val['rbe_right'],
            self.val['rbe_parent'],
            self.val['rbe_color']
        )


class ChainNodePrinter:
    """Print a Chain_Node structure."""
    def __init__(self, val):
        self.val = val

    def to_string(self):
        return "Chain_Node(next={}, previous={})".format(
            self.val['next'],
            self.val['previous']
        )


class WatchdogControlPrinter:
    """Print a Watchdog_Control structure."""
    def __init__(self, val):
        self.val = val

    def to_string(self):
        fields = []

        # Handle Node (RBTree or Chain)
        node = self.val['Node']
        if node['RBTree']['Node']['rbe_parent'] != 0:
            rbtree = RBTreeNodePrinter(node['RBTree']['Node'])
            fields.append("RBTree={}".format(rbtree.to_string()))
        else:
            chain = ChainNodePrinter(node['Chain'])
            fields.append("Chain={}".format(chain.to_string()))

        # Handle CPU field if defined
        if 'cpu' in self.val.type.keys():
            fields.append(f"cpu={self.val['cpu']}")

        # Handle routine field (function pointer)
        routine = self.val['routine']
        if routine:
            routine_str = gdb.execute(f"info symbol {routine}", to_string=True).strip()
            fields.append(f"routine={routine_str}")
        else:
            fields.append("routine=NULL")

        # Handle expire field
        fields.append(f"expire={self.val['expire']}")

        return "Watchdog_Control({})".format(", ".join(fields))


def register_watchdog_printers(objfile):
    # Register pretty printer for Watchdog_Control
    objfile.pretty_printers.append(
        lambda val: WatchdogControlPrinter(val) if str(val.type) == "Watchdog_Control" else None
    )


# Register the pretty-printer with the current objfile
gdb.printing.register_pretty_printer(gdb.current_objfile(), register_watchdog_printers)
