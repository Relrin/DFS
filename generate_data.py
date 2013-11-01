#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import random
import string

for i in xrange(0, 100):
    msg_length = random.randint(128, 512)
    message = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
                      for x in xrange(msg_length))
    file_name = str(i).rjust(3, '0')
    f = open('initial\\text-%s.txt' % file_name, 'w')
    f.write(message)
    f.close()