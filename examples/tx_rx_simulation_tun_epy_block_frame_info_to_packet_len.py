import numpy as np
import pmt
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(self,
            name='frame_info to packet_len',
            in_sig=[np.uint8],
            out_sig=[np.uint8])
        self.set_tag_propagation_policy(gr.TPP_DONT)
    def work(self, input_items, output_items):
        inp = input_items[0]
        out = output_items[0]
        n = len(inp)
        out[:n] = inp
        base_in = self.nitems_read(0)
        base_out = self.nitems_written(0)
        tags = self.get_tags_in_window(0, 0, n)
        for tag in tags:
            rel = tag.offset - base_in
            if rel < 0 or rel >= n:
                continue
            out_off = base_out + rel
            if pmt.symbol_to_string(tag.key) == 'frame_info':
                pay_len = pmt.to_long(pmt.dict_ref(tag.value, pmt.intern('pay_len'), pmt.PMT_NIL))
                if pay_len > 0:
                    self.add_item_tag(0, out_off, pmt.intern('packet_len'), pmt.from_long(pay_len))
            else:
                self.add_item_tag(0, out_off, tag.key, tag.value)
        return n
