#!/usr/bin/bash
# SPDX-License-Identifier: LGPL-2.1-or-later

# Trying to hide poymouth for unl0kr
# Can only hide plymouth if we wait long enough to show it
# TODO: Find way to do this without sleeping
sleep 5
plymouth hide-splash 2>/dev/null

# Searching for passwords for unl0kr
for file in `ls /run/systemd/ask-password/ask.*`; do
  socket="$(cat "$file" | grep "Socket=" | cut -d= -f2)"
  /usr/bin/unl0kr | /lib/systemd/systemd-reply-password 1 "$socket"
done

# Try to show Plymouth again after unl0kr
plymouth show-splash 2>/dev/null
