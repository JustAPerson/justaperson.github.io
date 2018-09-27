Title: Projects
Slug: about/projects


## [VOS][] (2015)

[VOS][] was my first venture in writing my own operating system. I didn't get
very far, as I was consumed by the minutia of trying to get Rust to compile for
16 bit protected mode--[going so far as recompiling many of the core libraries
myself][vosmake]. Perhaps the most interesting part of this project is the
reasonably complete and well documented [FAT filesystem implementation][vosfat]
I planned to use.

[vos]: https://github.com/JustAPerson/vos
[vosmake]: https://github.com/JustAPerson/vos/blob/rust_boot/makefile
[vosfat]: https://github.com/JustAPerson/vos/blob/master/src/lib/disk/src/fs/fat.rs

## [Denuos][] (2016)

[Denuos][] was my second attempt at writing my own operating system. This time I
got substantially farther. Some features implemented so far: basic VGA
rendering, keyboard and timer interrupts handled via PIC, dynamically allocated
memory, and the beginnings of a system call interface with working transitions
between privilege levels.

Ultimately, I believe the complexity of Rust is hindering this project, and I
intend to rewrite it in C. But first, I have to finish writing a preliminary
implementation [my own C compiler][denuoc].

[denuos]: https://github.com/JustAPerson/denuos
[denuoc]: https://github.com/JustAPerson/denuoc

## [LuaCrypt][lc] (2012)
    
As I've written about [elsewhere](/about/arcs/), I have an interest in
cryptography. I tried several times to implement basic security primitives in
Lua ([despite what everyone says][owncrypto]). I only successfully finished
SHA2. Eventually some one ended up finding [a bug in my code][lcbug] much to my
surprise that anyone ever even found my code, let alone used it.

[lc]: https://github.com/JustAPerson/LuaCrypt
[owncrypto]: http://lmgtfy.com/?q=writing+your+own+crypto
[lcbug]: https://github.com/JustAPerson/LuaCrypt/issues/1

## [Lua Bytecode Interpreter][lbi] (2012)

[LBI][lbi] was a project initiated out of necessity. I began programming because
of an online game called [Roblox][roblox], which can vaguely be described as a
platform for kids to create lego-like games that are scripted using Lua. Roblox
creators often utilized a technique of obfuscation whereby they uploaded their
scripts as precompiled bytecode in order to prevent introspection or
modification. This was a form of copy-protection because scripts were ran on the
user's computer and could be read from memory and then used to create a
competing game. In 2012, Roblox removed the `loadstring()` function that enabled
the loading of bytecode. Thus, by implementing this project I was hoping to
salvage scripts I and many others had already precompiled.

This functionality was removed because specially crafted bytecode can exploit
the internal state of the Lua virtual machine and potentially whatever C
application is using it. These attacks are documented [here][corsix]. I
attempted to apply some of these attacks to Roblox, but didn't find any C
functions that seemed exploitable. However, I did encounter several
modifications the Roblox developers had made to harden the VM, including adding
read-only tables (as an atomic type, not accomplished through [metatables][mt]).

I emailed one of the lead developers about both my findings and the original
documentation of these bugs on 22 August 2011. They largely ignored my findings
at the time because I had not actually found a useful way to exploit the game.
Almost exactly one year later, [Roblox announced the removal of
`loadstring`][byebyebc]. Someone else had found a Roblox API that was vulnerable
to this exploit.

[lbi]: https://github.com/JustAPerson/lbi
[roblox]: https://en.wikipedia.org/wiki/Roblox
[corsix]: https://www.corsix.org/content/lua-514-bug-recap
[mt]: https://www.lua.org/pil/13.html
[byebyebc]: https://blog.roblox.com/2012/08/bye-bye-bytecode/

## [Maximum Overdrive System][mods] (2011)

[MODS][mods] is a Lua bytecode assembler and disassembler.

[mods]: https://github.com/JustAPerson/MODS

## [Brainrust][br] (2015)

[Brainrust][br] is a simple [Brainfuck][bf] interpreter. It performs some
obvious reductions in repetitive instructions. Similarly, [brain86][b86] is a
trivial 60 line program I wrote to translate Brainfuck to x86 assembly.

[bf]: https://en.wikipedia.org/wiki/Brainfuck
[br]: https://github.com/JustAPerson/brainrust
[b86]: https://gist.github.com/JustAPerson/8fe97f1591153a070cc5

