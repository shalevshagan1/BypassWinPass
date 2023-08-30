# sudo apt install genisoimage grub
# get stage2_eltrino from https://littleosbook.github.io/files/stage2_eltorito
import os
import shutil
import requests
import tarfile
import subprocess

BUSYBOX_VERSION = "busybox-1.36.1"
BUSYBOX_EXTENSIONS = ".tar.bz2"

KERNEL_VERSION = subprocess.check_output("uname -r", shell=True, text=True)[:-1] # tested with 6.2.0-31-generic

def make_initramfs():
    # Create initramfs
    directories = ["bin", "dev", "etc", "home", "lib", "lib64", "mnt", "proc", "root", "sbin", "sys", "usr"]
    for directory in directories:
        os.makedirs(os.path.join("initramfs", directory), exist_ok=True)

    shutil.copy("./assets/init", "initramfs")
    shutil.copy("./assets/sethc.exe", "initramfs")

    # cd initramfs/dev
    #sudo mknod sda b 8 0 
    # sudo mknod console c 5 1


def make_busybox():
    # TODO - Check which tools are requried to compile it
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
        subprocess.run(["make"], cwd=BUSYBOX_VERSION, check=True)
        subprocess.run(["make", "CONFIG_PREFIX=../initramfs", "install"], cwd=BUSYBOX_VERSION, check=True)
    except subprocess.CalledProcessError as e:
        pass 


def get_drivers():
    os.makedirs(f"./initramfs/lib/modules/{KERNEL_VERSION}/kernel/drivers/ata/", exist_ok=True)

    shutil.copy(f"/lib/modules/{KERNEL_VERSION}/kernel/drivers/ata/libahci.ko",  f"./initramfs/lib/modules/{KERNEL_VERSION}/kernel/drivers/ata/libahci.ko")
    shutil.copy(f"/lib/modules/{KERNEL_VERSION}/kernel/drivers/ata/ahci.ko",  f"./initramfs/lib/modules/{KERNEL_VERSION}/kernel/drivers/ata/ahci.ko")

# TODO copy lsblk and blkid and their deps

def make_iso():
    os.makedirs("./iso/boot/grub")
    #shutil.copy("")

    # copy vmlinuz to /iso/boot
#     cp ./initramfs.cpio.gz iso/boot/initramfs.cpio.gz

#     # copy menu.lst to /iso/boot/grub
#     # copy stage2_eltorito to /iso/boot/grub

#     sudo genisoimage -R                         \
#                 -b boot/grub/stage2_eltorito    \
#                 -no-emul-boot                   \
#                 -boot-load-size 4               \
#                 -A os                           \
#                 -input-charset utf8             \
#                 -quiet                          \
#                 -boot-info-table                \
#                 -o os.iso                       \
#                 iso


# rm ../initramfs.cpio
# rm ../initramfs.cpio.gz
# rm ../os.iso

# find . -print0 | cpio --null -ov --format=newc > ../initramfs.cpio 
# cd ..
# gzip ./initramfs.cpio

# cp -aLR /lib/x86_64-linux-gnu/{libblkid.so.1,libmount.so.1,libsmartcols.so.1,libudev.so.1,libc.so.6,libselinux.so.1,libpcre2-8.so.0} ~/Desktop/initramfs/lib/x86_64-linux-gnu
# cp -aLR /lib64/ld-linux-x86-64.so.2 /home/shalev/Desktop/initramfs/lib64

def main():
    #make_initramfs() # Works!
    #make_busybox() # Works!
    #get_drivers() # Works!
    make_iso() 


main()