#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of zero-ears.
#
# zero-ears is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# zero-ears is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with zero-ears.  If not, see <http://www.gnu.org/licenses/>.
# Author: Jérôme ORNECH alias "Tuux" <tuxa@rtnp.org>

import zmq
from ears import Ears

zmq_ctx = zmq.Context()

publish_zmq_channel = "ipc:///tmp/zero_ears_bus"

publish_zmq_socket = zmq_ctx.socket(zmq.PUB)
publish_zmq_socket.bind(publish_zmq_channel)

ears = Ears(publish_zmq_socket)

while True:
    print "zero-ears loop"

    # FIXME: change for meaningful event
    publish_zmq_socket.send(">ears>prompt>type=1")

    recognizing = ears.decode_speech(
        ears.acoustic_model_directory,
        ears.language_model_file,
        ears.dictionary_file,
        ears.wavfile
    ).strip()

    if recognizing:
        print "zero-ears:perceive:"+recognizing
        message = ">ears>perceive>" + recognizing
        publish_zmq_socket.send(message)
