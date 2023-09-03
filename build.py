#!/usr/bin/python3
import os
import shutil
import requests
import tarfile
import subprocess

BUSYBOX_VERSION = "busybox-1.36.1"
BUSYBOX_EXTENSIONS = ".tar.bz2"

KERNEL_VERSION = subprocess.check_output(["uname", "-r"], text=True)[:-1] # tested with 6.2.0-31-generic

def make_initramfs():
    # Create initramfs
    directories = ["bin", "dev", "etc", "home", "lib", "lib64", "mnt", "proc", "root", "sbin", "sys", "usr"]
    for directory in directories:
        os.makedirs(os.path.join("initramfs", directory), exist_ok=True)

    shutil.copy("./assets/init", "initramfs")
    with open("./initramfs/init", 'r') as file:
        content = file.read()
    content = content.replace("KERNEL_VERSION_PLACEHOLDER", KERNEL_VERSION)
    with open("./initramfs/init", 'w') as file:
        file.write(content)

    shutil.copy("./assets/sethc.exe", "initramfs")


def make_busybox():
    # TODO - Check which tools are requried to compile busybox
    resp = requests.get(f"https://www.busybox.net/downloads/{BUSYBOX_VERSION + BUSYBOX_EXTENSIONS}")
    with open(BUSYBOX_VERSION + BUSYBOX_EXTENSIONS, "wb") as file:
        file.write(resp.content)
    with tarfile.open(BUSYBOX_VERSION + BUSYBOX_EXTENSIONS, 'r') as tar:
        tar.extractall()

    try:
        subprocess.run(["make", "defconfig"], check=True, cwd=BUSYBOX_VERSION)
    except subprocess.CalledProcessError as e:
        pass

    # Config BusyBox to build staticly  
    with open(f"{BUSYBOX_VERSION}/.config", 'r') as file:
        content = file.read()
    content = content.replace("# CONFIG_STATIC is not set", "CONFIG_STATIC=y")
    with open(f"{BUSYBOX_VERSION}/.config", 'w') as file:
        file.write(content)

    try:
        # TODO direct output
        subprocess.run(["make"], cwd=BUSYBOX_VERSION, check=True)
        subprocess.run(["make", "CONFIG_PREFIX=../initramfs", "install"], cwd=BUSYBOX_VERSION, check=True)
    except subprocess.CalledProcessError as e:
        pass 


def add_program_and_depends(name):
    fullpath = subprocess.check_output(["which", name], text=True)[:-1]

    ldd_proc = subprocess.Popen(["ldd", fullpath], stdout=subprocess.PIPE, text=True)    
    grep_proc = subprocess.Popen(["grep", "-o", '/[^ ]*'], stdin=ldd_proc.stdout, stdout=subprocess.PIPE, text=True)
    ldd_proc.stdout.close()

    depends_path = grep_proc.communicate()[0].split('\n')

    # copy dependencies
    for systempath in depends_path:
        locallibpath = os.path.join("./initramfs", systempath[1:])
        if not os.path.exists(locallibpath):
            os.makedirs(os.path.dirname(locallibpath), exist_ok=True)
            shutil.copy(systempath, locallibpath)

    # copy binary
    localbinarypath = os.path.join("./initramfs", fullpath[1:])
    os.makedirs(os.path.dirname(localbinarypath), exist_ok=True)
    shutil.copy(fullpath, localbinarypath)


def make_diskutils():
    add_program_and_depends("bash")
    add_program_and_depends("blkid")
    add_program_and_depends("lsblk")
    add_program_and_depends("ntfs-3g")
    add_program_and_depends("ntfsfix")


def get_drivers():
    os.makedirs(f"./initramfs/lib/modules/{KERNEL_VERSION}/kernel/drivers/ata/", exist_ok=True)

    shutil.copy(f"/lib/modules/{KERNEL_VERSION}/kernel/drivers/ata/libahci.ko",  f"./initramfs/lib/modules/{KERNEL_VERSION}/kernel/drivers/ata/libahci.ko")
    shutil.copy(f"/lib/modules/{KERNEL_VERSION}/kernel/drivers/ata/ahci.ko",  f"./initramfs/lib/modules/{KERNEL_VERSION}/kernel/drivers/ata/ahci.ko")


def make_iso():
    # Compress initramfs
    subprocess.run("find . -print0 | cpio --null -o --format=newc > ../initramfs.cpio", shell=True, cwd="./initramfs")
    subprocess.run(["gzip", "./initramfs.cpio"])

    os.makedirs("./iso/boot/grub", exist_ok=True)

    try:
        subprocess.run(["sudo", "cp", "-av", f"/boot/vmlinuz-{KERNEL_VERSION}", "./iso/boot/vmlinuz"], check=True) # Copying the Kernel requires root, but I don't want the entire script to require it
    except subprocess.CalledProcessError as e:
        pass 

    shutil.copy(f"initramfs.cpio.gz", "./iso/boot")

    shutil.copy(f"./assets/menu.lst", "./iso/boot/grub")
    resp = requests.get("https://littleosbook.github.io/files/stage2_eltorito")
    with open("./iso/boot/grub/stage2_eltorito", 'ab') as file:
        file.write(resp.content)

    cmd = command = [
        "sudo", "genisoimage",
        "-R",
        "-b", "boot/grub/stage2_eltorito",
        "-no-emul-boot",
        "-boot-load-size", "4",
        "-A", "C00LOS",
        "-input-charset", "utf8",
        "-quiet",
        "-boot-info-table",
        "-o", "C00LOS.iso",
        "./iso/"
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        pass 

def cleanup():
    # TODO - check if file/dir exist
    shutil.rmtree("iso")
    shutil.rmtree("initramfs")
    os.remove("initramfs.cpio.gz")
    os.remove("os.iso")


def main():
    # sudo apt install genisoimage lsblk blkid ntfs-3g ntfsfix
    #cleanup()
    make_initramfs() # Works!
    make_busybox() # Works!
    get_drivers() # Works!
    make_diskutils() # Works!
    make_iso()  # Works!

if __name__ == "__main__":
    main()