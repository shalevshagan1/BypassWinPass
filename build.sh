# sudo apt install genisoimage grub
# get stage2_eltrino from https://littleosbook.github.io/files/stage2_eltorito


# Create initramfs
# mkdir -p initramfs/{bin,dev,etc,home,mnt,proc,sys,usr}
# copy init from assets
# copy sethc from assets
# cd initramfs/dev
#sudo mknod sda b 8 0 
# sudo mknod console c 5 1

# Get BusyBox
# wget https://busybox.net/downloads/...
# tar -xvf busybox-1.26.2.tar.bz2
#cd busybox-1.26.2
#make defconfig
#make menuconfig
# Config BusyBox to build staticly
#make
# make CONFIG_PREFIX=./../busybox_rootfs install


rm ../initramfs.cpio
rm ../initramfs.cpio.gz
rm ../os.iso

find . -print0 | cpio --null -ov --format=newc > ../initramfs.cpio 
cd ..
gzip ./initramfs.cpio


mkdir -p iso/boot/grub
# copy vmlinuz to /iso/boot
cp ./initramfs.cpio.gz iso/boot/initramfs.cpio.gz

# copy menu.lst to /iso/boot/grub
# copy stage2_eltorito to /iso/boot/grub


sudo genisoimage -R                         \
            -b boot/grub/stage2_eltorito    \
            -no-emul-boot                   \
            -boot-load-size 4               \
            -A os                           \
            -input-charset utf8             \
            -quiet                          \
            -boot-info-table                \
            -o os.iso                       \
            iso
            
     
#read        

#sudo qemu-system-x86_64 -nographic -hda os.iso -initrd ./initramfs.cpio.gz -kernel /boot/vmlinuz-6.2.0-26-generic -append 'console=ttyS0 root=/dev/sda'

# cp -aLR /lib/x86_64-linux-gnu/{libblkid.so.1,libmount.so.1,libsmartcols.so.1,libudev.so.1,libc.so.6,libselinux.so.1,libpcre2-8.so.0} ~/Desktop/initramfs/lib/x86_64-linux-gnu
# cp -aLR /lib64/ld-linux-x86-64.so.2 /home/shalev/Desktop/initramfs/lib64

# copy drivers

# mkdir -p lib/modules/6.2.0-26-generic/kernel/drivers/ata
# cp -pv /lib/modules/6.2.0-26-generic/kernel/drivers/ata/{ahci.ko,libahci.ko} lib/modules/6.2.0-26-generic/kernel/drivers/ata/


