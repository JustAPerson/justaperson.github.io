---
title: Using `setxkbmap`
date: 2019-12-17
---

After using Ubuntu for a number of years, I was quite accustomed to customizing
my desktop experience using the GUI tools provided by GNOME. In the past year, I
have been using [awesome][], a tiling window manager. Some things can still be
configured using the `gnome-control-center` application, but I have also been
experimenting more with using the underlying technologies that GNOME uses behind
the scenes.

[awesome]: https://awesomewm.org/

Today, I wanted to change my keyboard settings so I can type moderately fancy
letters like `éàîöŭ`. There are two common ways to approach this, and which you
choose probably depends on the frequency you need such characters. First, you
can use a __compose key__, so that you type a combination like `Compose ' e` to
get `é`. Second, you can use __dead keys__, where typing one of the prefixes
like `'` enters a state where you can type another letter like any of `aiueo` to
get `áíúéó` respectively or you can type `'` again to get that actual single
quote character. Since I don't foresee needing to type _that_ much using these
characters, I went with a compose key. Additionally, I will also describe how to
enable dead keys for a US keyboard.

From what I've learned, the easiest way to accommodate this is to use the
existing Debian keyboard config files. You can read about the semantics in the
`keyboard(5)` manpage. The system wide file is `/etc/default/keyboard`, but it
appears `~/.keyboard` should also work. This file is a list of variables that
looked like this by default for me:

```bash
# KEYBOARD CONFIGURATION FILE
# Consult the keyboard(5) manual page.

XKBMODEL="pc105"
XKBLAYOUT="us"
XKBVARIANT=""
XKBOPTIONS=""
BACKSPACE="guess"
```

For enabling dead keys, it appears as simple as setting `XKBVARIANT="intl"`. For
choosing a compose key, we would like to modify `XKBOPTIONS`. There are a lot
options to choose from, but the ones relevant to us are the following:

```text
$ grep "compose:" /usr/share/X11/xkb/rules/xorg.lst
  compose:ralt         Right Alt
  compose:lwin         Left Win
  compose:lwin-altgr   3rd level of Left Win
  compose:rwin         Right Win
  compose:rwin-altgr   3rd level of Right Win
  compose:menu         Menu
  compose:menu-altgr   3rd level of Menu
  compose:lctrl        Left Ctrl
  compose:lctrl-altgr  3rd level of Left Ctrl
  compose:rctrl        Right Ctrl
  compose:rctrl-altgr  3rd level of Right Ctrl
  compose:caps         Caps Lock
  compose:caps-altgr   3rd level of Caps Lock
  compose:102          &lt;Less/Greater&gt;
  compose:102-altgr    3rd level of &lt;Less/Greater&gt;
  compose:paus         Pause
  compose:prsc         PrtSc
  compose:sclk         Scroll Lock
```

I chose to use Right Alt. In addition, I prefer to change the semantics of the
capslock key, and there are several options for that. Ultimately, I set
`XKBOPTIONS="compose:ralt,caps:ctrl_modifier"` in `~/.keyboard`.

# Going Further

I decide while I was playing with keyboard configurations, I would attempt to
fix a minor inconvenience I've experienced. I primarily use a wireless keyboard
to type on my laptop. The wireless and internal keyboards have slightly
different layouts. The internal keyboard has the super key to the left of the
spacebar whereas the wireless keyboard has the alt key in that position. Thus,
I'd like to switch these keys around on __only one__ device. This cannot be
achieved using the `~/.keyboard` file as far as I can tell.

`setxkbmap` is a utility that can set the same parameters as the variables
accepted by the `~/.keyboard` file. More importantly, `setxkbmap` can configure a
specific X device using the `-device` flag. We can invoke `setxkbmap` inside the
`~/.xinitrc` script that will be executed by any X session.

First, we use `xinput` to print the available input devices:
```text
$ xinput
⎡ Virtual core pointer                          id=2    [master pointer  (3)]
⎜   ↳ Virtual core XTEST pointer                id=4    [slave  pointer  (2)]
⎜   ↳ bcm5974                                   id=11   [slave  pointer  (2)]
⎜   ↳ Logitech M570                             id=12   [slave  pointer  (2)]
⎜   ↳ Logitech K400 Plus                        id=13   [slave  pointer  (2)]
⎣ Virtual core keyboard                         id=3    [master keyboard (2)]
    ↳ Virtual core XTEST keyboard               id=5    [slave  keyboard (3)]
    ↳ Power Button                              id=6    [slave  keyboard (3)]
    ↳ Video Bus                                 id=7    [slave  keyboard (3)]
    ↳ Power Button                              id=8    [slave  keyboard (3)]
    ↳ Sleep Button                              id=9    [slave  keyboard (3)]
    ↳ Apple Inc. Apple Internal Keyboard / Trackpad     id=10   [slave  keyboard (3)]
    ↳ Logitech K400 Plus                        id=14   [slave  keyboard (3)]
```

We want to select two of the _slave keyboards_. There's probably a better way to
extract the device id, but I used `grep` and `sed` like so:

```bash
kb1=$(xinput | grep -E "Logitech K400 Plus.+keyboard" | sed -E "s/^.*id=([0-9]+).*$/\1/")
kb2=$(xinput | grep -E "Apple Inc.+keyboard" | sed -E "s/^.*id=([0-9]+).*$/\1/")
```

I prefer having super, which I use more often, close to the space bar, so I want
 to swap them on the wireless keyboard. In addition to the other values from the
 `XKBOPTIONS` variable from our `~/.keyboard`, I can use the
 `altwin:swap_lalt_lwin` option to achieve the desired behavior.
 
 There are two remaining details. Whereas the `~/.keyboard` file accepts a
 comma-separated list of options, we must pass each option as a separate flag to
 `setxkbmap`. Additionally, it seems we must first clear all the options using
 `-option ""` before we can set device-specific options. Otherwise both devices
 end up with the union of their options it seems.

Thus finally, my `~/.xinitrc` script looks like so:

```bash
kb1=$(xinput | grep -E "Logitech K400 Plus.+keyboard" | sed -E "s/^.*id=([0-9]+).*$/\1/")
kb2=$(xinput | grep -E "Apple Inc.+keyboard" | sed -E "s/^.*id=([0-9]+).*$/\1/")

setxkbmap -device $kb1 -layout us -option "" -option compose:ralt \
                                  -option caps:ctrl_modifier      \
                                  -option altwin:swap_lalt_lwin
setxkbmap -device $kb2 -layout us -option "" -option compose:ralt \
                                  -option caps:ctrl_modifier
```

# Making Things Work

With the `~/.xinitrc` script in place, you can either execute it manually or log
in again. It should now be possible to use the compose key in every application.
Well, everything except Emacs it seems. This issue seems to date back ten
years[^1], rediscovered on the emacs-devel list five years ago[^2] and allegedly
fixed[^3] around version 24.4. However, when I press the compose key in Emacs
25.2.2 graphical window (not in a terminal), the compose key does not work and
instead I get a message that `<Multi_key> is undefined`.

[^1]: <https://bugs.launchpad.net/ubuntu/+source/emacs23/+bug/493766>
[^2]: <https://lists.gnu.org/archive/html/emacs-devel/2014-03/msg00867.html>
[^3]: <https://lists.gnu.org/archive/html/emacs-devel/2014-03/msg00881.html>

The simplest solution is to create the following wrapper script somewhere early in your `$PATH` like  `~/.local/bin/emacs`:

```bash
#!/bin/bash
env -u XMODIFIERS /usr/bin/emacs $@
```
