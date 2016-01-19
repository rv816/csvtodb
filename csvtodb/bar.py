#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

from __future__ import division
from __future__ import print_function
def old_div(val1, val2):
    return float(val1) / float(val2)
# Copyright (c) 2012 Giorgos Verigakis <verigak@gmail.com>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


# EnhancedBar Added by Ryan Vass

from  etl_modules.progress.progress import Progress
from etl_modules.progress.progress.helpers import WritelnMixin
from collections import OrderedDict
import time
import datetime

class Bar(WritelnMixin, Progress):
    width = 32
    message = ''
    suffix = '%(index)d/%(max)d'
    bar_prefix = ' |'
    bar_suffix = '| '
    empty_fill = ' '
    fill = '#'
    hide_cursor = True

    def update(self):
        filled_length = int(self.width * self.progress)
        empty_length = self.width - filled_length

        message = self.message % self
        bar = self.fill * filled_length
        empty = self.empty_fill * empty_length
        suffix = self.suffix % self
        line = ''.join([message, self.bar_prefix, bar, empty, self.bar_suffix,
                        suffix])
        self.line = line
        self.writeln(line)





class EnhancedBar(Bar):
    #def __init__(self, *args, **kwargs):
     #   super(EnhancedBar, self).__init__()
        #self.barstring = str(self.message) + str(b.bar_prefix + '{progressbar}' + b.bar_suffix)

        #self.max = max
        #self.fill_tup = (self.fill)*int(self.progress * 100)
        #self.empty_tup = (' ')*(100 - len(self.fill_tup))
        #self.progress_tup = tuple(self.fill_tup + self.empty_tup)
        #self.printable_bar = self.barstring.format(x for x in self.progress_tup)


    def time_delta(self, resolution='miliseconds', return_dict=False):
        '''From seconds to Days;Hours:Minutes;Seconds;Miliseconds'''
        elapsed_seconds = time.time() - self.start_ts
        value = elapsed_seconds

        valueD = (old_div((old_div((old_div(value,365)),24)),60))
        Days = int (valueD)

        valueH = (valueD-Days)*365
        Hours = int(valueH)

        valueM = (valueH - Hours)*24
        Minutes = int(valueM)

        valueS = (valueM - Minutes)*60
        Seconds = int(valueS)

        valueMS = (valueS - Seconds)*1000
        Miliseconds = int(valueMS)

        valueUS = (valueMS - Miliseconds)*1000
        Microseconds = int(valueUS)


        elapsed_seconds = time.time() - self.start_ts
        self.elapsed_seconds = elapsed_seconds
        total_elapsed_microseconds = Microseconds + (elapsed_seconds) * 10**6

        self.resolution = resolution

        if resolution=='seconds':
            total_elapsed = old_div(float(total_elapsed_microseconds), float(10**9))
        elif resolution == 'miliseconds':
            total_elapsed = old_div(float(total_elapsed_microseconds), float(10**6))
        elif resolution == 'microseconds':
            total_elapsed = total_elapsed_microseconds
        else:
            total_elapsed = total_elapsed_microseconds

        self.elapsed_timedict = OrderedDict({'days': Days,
                    'hours':Hours,
                    'minutes': Minutes,
                    'seconds': Seconds,
                    'miliseconds': Miliseconds,
                    'microseconds': Microseconds})

        setattr(self, 'total_elapsed', total_elapsed)

        if return_dict:
            return self.elapsed_timedict
        else:
            return total_elapsed


    def update(self):
        filled_length = int(self.width * self.progress)
        empty_length = self.width - filled_length

        message = self.message % self
        bar = self.fill * filled_length
        empty = self.empty_fill * empty_length
        suffix = self.suffix % self
        line = ''.join([message, self.bar_prefix, bar, empty, self.bar_suffix,
                        suffix])
        self.line = line
        self.tracker = self.print_bar()
        print(self.tracker)
        self.writeln(line)

    def calculate_velocity(self):
        turns = float(self.index)
        total_time = float(self.time_delta())
        time_per_turn = old_div(total_time, turns)
        return time_per_turn # by default, this is in microseconds per turn


    def print_bar(self):
        self.statstring = '{line} \n' + '\t\t {index} out of {total}, {secs} miliseconds per iteration \n \t\t {minutes} minutes remaining'
        self.fillstring = self.fill*int(old_div(float(self.index), float(self.max)))*100
        self.emptystring = ' '*(100 - len(self.fillstring))
        self.progress_tup = (self.fillstring + self.emptystring)
        self.speed = self.calculate_velocity()
        num_remaining = self.max - self.index
        self.minutes_remaining = num_remaining * float(self.speed)/float((1000*60))
        #self.printable_bar = self.barstring.format(progressbar = self.progress_tup, index = self.index, total=self.max, secs = self.speed)
        self.printable_bar = self.statstring.format(line=self.line, index = self.index, total=self.max, secs = self.speed, minutes=self.minutes_remaining)
        return self.printable_bar








class ChargingBar(Bar):
    suffix = '%(percent)d%%'
    bar_prefix = ' '
    bar_suffix = ' '
    empty_fill = u'∙'
    fill = u'█'


class FillingSquaresBar(ChargingBar):
    empty_fill = u'▢'
    fill = u'▣'


class FillingCirclesBar(ChargingBar):
    empty_fill = u'◯'
    fill = u'◉'


class IncrementalBar(Bar):
    phases = (u' ', u'▏', u'▎', u'▍', u'▌', u'▋', u'▊', u'▉', u'█')

    def update(self):
        nphases = len(self.phases)
        expanded_length = int(nphases * self.width * self.progress)
        filled_length = int(self.width * self.progress)
        empty_length = self.width - filled_length
        phase = expanded_length - (filled_length * nphases)

        message = self.message % self
        bar = self.phases[-1] * filled_length
        current = self.phases[phase] if phase > 0 else ''
        empty = self.empty_fill * max(0, empty_length - len(current))
        suffix = self.suffix % self
        line = ''.join([self.message, self.bar_prefix, bar, current, empty,
                        self.bar_suffix, suffix])
        self.writeln(line)


class ShadyBar(IncrementalBar):
    phases = (u' ', u'░', u'▒', u'▓', u'█')
