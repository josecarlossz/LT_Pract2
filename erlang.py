"""
The MIT License (MIT)

Copyright (c) 2014 Nate Mara

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from __future__ import division


def extended_b_lines(usage, blocking):
	'''
	Uses the Extended Erlang B formula to calcluate the ideal number of lines
	for the given usage in erlangs and the given blocking rate.

	Usage:
	extended_b_lines(usage, blocking)
	'''

	line_count = 1
	while extended_b(usage, line_count) > blocking:
		line_count += 1
	return line_count


def extended_b(usage, lines, recall=0):
	'''
	Usage:
	extended_b(usage, lines, recall=0)
	'''

	original_usage = usage
	while True:
		PB = b(usage, lines)
		magic_number_1 = (1 - PB) * usage + (1 - recall) * PB * usage
		magic_number_2 = 0.9999 * original_usage
		if magic_number_1 >= magic_number_2:
			return PB
		usage = original_usage + recall * PB * usage
	return -1


def b(usage, lines):
	'''
	Usage:
	b(usage, lines)
	'''

	if usage > 0:
		PBR = (1 + usage) / usage
		for index in range(2, lines + 1):
			PBR = index / usage * PBR + 1
			if PBR > 10000:
				return 0
		return 1 / PBR
	return 0
