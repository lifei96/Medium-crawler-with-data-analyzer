# encoding: utf-8
import codecs
import os
import medium_u_analyser_random

for i in range(1, 100):
	Str = "No.%d"%i + medium_u_analyser_random.Get(5)
	Result_output = codecs.open("./Result_analyser_random.txt", 'a+', 'utf-8')
	Result_output.write(Str)
	Result_output.close()
