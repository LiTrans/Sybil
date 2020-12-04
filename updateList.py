

from optparse import OptionParser


def run(node):
	with open('done_list.txt','r') as f:
		tmp = f.readline()
		done = eval(tmp)
		f.close()
	done.append(node)
	with open('done_list.txt','w') as out:
		out.write('{}'.format(done)+ '\n')
		out.write('Total {}'.format(len(done)))
		out.close()
		f.close()
		
if __name__ == "__main__":	
	options = OptionParser()
	options.add_option("-n", "--node", help = "node", dest="node")
	(opt,arg) = options.parse_args()
	
	run(opt.node)