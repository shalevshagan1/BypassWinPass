# Bypass Windows Password
This software can bypass Windows' password!

Firstly, I want to mention that this is a hobby project intended for learning Linux (How does one learn Linux from such a project? Let's find out). You can easily accomplish the goal of this project by booting from a LIVE CD of any Linux distribution, mounting Windows' drive and replacing the necessary file.

DISCLAIMER! This software must not serve as an offensive tool; it's for EDUCATIONAL PURPOSES ONLY!

# When does it work?
To make it work, a few conditions must be met:
- The disk must not use BitLocker encryption (or if you know BitLocker's password, a live CD is your choice).
- (Check for MS account availability)

# How does it work?
When you boot the ISO, it loads the Initial RAM Filesystem, typically used in Linux to prepare the system for boot. But that's boring. We use it because of its comfortable characteristics: It operates outside of Windows, allowing us to modify Windows' files, and it loads into RAM, making it similar to a LiveCD but much lighter and automatic.

Anyway, on Windows, a 'feature' called "Sticky Keys" triggered when you press Shift 5 times. Who cares? Well, if you're logged in, no one. But if you're locked out of your system, you're in luck.
When activated on the Lock Screen, the Sticky Keys executeable runs with SYSTEM Privilege, meaning that if we can replace the executeable, we can launch a Command Prompt as Administrator and run a command to REMOVE the user's password.


TODO
- [] compile staticly with all libraries
- [] add 32 bit support
- [] add support for unicode Account names
- [] add Linux support
