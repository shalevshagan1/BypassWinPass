# Bypass Windows Password
This software can bypass Windows's password!

# When does it work?
First of all, a few conditions for it to work

- The Disk must not be encrypted with BitLocker, or you know the password
- (Check availability for MS account)

# How does it work?

When you boot the ISO, it run linux initramfs, a minimal file system that loaded into RAM...

It replaces the sethc.exe file, with our own sethc, that runs "echo | net user USERNAME "

Here's the intersting part:
As you probably wondered, "how are we supposed to run this sethc?" and the pros woundered "net requires admin"

It uses the "sethc vuln" in

when pressing shift five times from lock screen, it open the "sethc.exe" exeuctable for "Sticky Keys",
and the best part, it runs on the highest level of system access "NT_AUTHORITY"

after the elevated shell ran the command, the password is gone!


TODO
compile staticly with all libraries
add support for bitlocked drives when user knows the password (Maybe read the key from disk as suggested?)
add 32 bit support
add support for unicode Account names