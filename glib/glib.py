import gdb

# This is not quite right, as local vars may override symname
def read_global_var (symname):
    return gdb.selected_frame().read_var(symname)

def g_quark_to_string (quark):
    if quark == None:
        return None
    quark = long(quark)
    if quark == 0:
        return None
    val = read_global_var ("g_quarks")
    max_q = long(read_global_var ("g_quark_seq_id"))
    if quark < max_q:
        return val[quark].string()
    return None

# We override the node printers too, so that node->next is not expanded
class GListNodePrinter:
    "Prints a GList node"

    def __init__ (self, val):
        self.val = val

    def to_string (self):
        return "{data=%s, next=0x%x, prev=0x%x}" % (str(self.val["data"]), long(self.val["next"]), long(self.val["prev"]))

class GSListNodePrinter:
    "Prints a GSList node"

    def __init__ (self, val):
        self.val = val

    def to_string (self):
        return "{data=%s, next=0x%x}" % (str(self.val["data"]), long(self.val["next"]))

class GListPrinter:
    "Prints a GList"

    class _iterator:
        def __init__(self, head, listtype):
            self.link = head
            self.listtype = listtype
            self.count = 0

        def __iter__(self):
            return self

        def next(self):
            if self.link == 0:
                raise StopIteration
            data = self.link['data']
            self.link = self.link['next']
            count = self.count
            self.count = self.count + 1
            return ('[%d]' % count, data)

    def __init__ (self, val, listtype):
        self.val = val
        self.listtype = listtype

    def children(self):
        return self._iterator(self.val, self.listtype)

    def to_string (self):
        return  "0x%x" % (long(self.val))

    def display_hint (self):
        return "array"

class GHashPrinter:
    "Prints a GHashTable"

    class _iterator:
        def __init__(self, ht, keys_are_strings):
            self.ht = ht
            if ht != 0:
                self.array = ht["nodes"]
                self.size = ht["size"]
            self.pos = 0
            self.keys_are_strings = keys_are_strings
            self.value = None

        def __iter__(self):
            return self

        def next(self):
            if self.ht == 0:
                raise StopIteration
            if self.value != None:
                v = self.value
                self.value = None
                return v
            while long(self.pos) < long(self.size):
                node = self.array[self.pos]
                self.pos = self.pos + 1
                if long (node["key_hash"]) >= 2:
                    key = node["key"]
                    val = node["value"]

                    if self.keys_are_strings:
                        key = key.cast (gdb.lookup_type("char").pointer())

                    # Queue value for next result
                    self.value = ('[%dv]'% (self.pos), val)

                    # Return key
                    return ('[%dk]'% (self.pos), key)
            raise StopIteration

    def __init__ (self, val):
        self.val = val
        self.keys_are_strings = False
        try:
            string_hash = read_global_var ("g_str_hash")
        except:
            try:
                string_hash = read_global_var ("IA__g_str_hash")
            except:
                string_hash = None
        if self.val != 0 and string_hash != None and self.val["hash_func"] == string_hash:
            self.keys_are_strings = True

    def children(self):
        return self._iterator(self.val, self.keys_are_strings)

    def to_string (self):
        return  "0x%x" % (long(self.val))

    def display_hint (self):
        return "map"

def pretty_printer_lookup (val):
    if is_g_type_instance (val):
        return GTypePrettyPrinter (val)

def pretty_printer_lookup (val):
    # None yet, want things like hash table and list

    type = val.type.unqualified()

    # If it points to a reference, get the reference.
    if type.code == gdb.TYPE_CODE_REF:
        type = type.target ()

    if type.code == gdb.TYPE_CODE_PTR:
        type = type.target().unqualified()
        t = str(type)
        if t == "GList":
            return GListPrinter(val, "GList")
        if t == "GSList":
            return GListPrinter(val, "GSList")
        if t == "GHashTable":
            return GHashPrinter(val)
    else:
        t = str(type)
        if t == "GList":
            return GListNodePrinter(val)
        if t == "GSList *":
            return GListPrinter(val, "GSList")
    return None

def register (obj):
    if obj == None:
        obj = gdb

    obj.pretty_printers.append(pretty_printer_lookup)