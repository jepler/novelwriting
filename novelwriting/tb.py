import traceback, sys
def format_one_frame(t):
	if not t.tb_frame.f_locals.has_key("self"):
		traceback.print_tb(t, 1)
		return
	s = t.tb_frame.f_locals['self']
	print >>sys.stderr, "  Expanding", repr(s)

def novelwriting_except_hook(ec, c, t):
	global gec, gc, gt
	gec, gc, gt = ec, c, t
	print "Traceback (most recent call last):"
	while t:
		format_one_frame(t)
		t = t.tb_next
	print c

sys.excepthook = novelwriting_except_hook
