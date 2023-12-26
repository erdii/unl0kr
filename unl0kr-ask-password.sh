#!/usr/bin/bash
# SPDX-License-Identifier: LGPL-2.1-or-later

plymouth hide-splash 2>/dev/null

for file in `ls /run/systemd/ask-password/ask.*`; do
  socket="$(cat "$file" | grep "Socket=" | cut -d= -f2)"
  /usr/bin/unl0kr | /lib/systemd/systemd-reply-password 1 "$socket"
done

plymouth show-splash 2>/dev/null

