
## for swan

def reboot_bootloader():
    
adb shell "reboot bootloader"

==========VTS==========
fastboot flashing unlock
fastboot flashing unlock_critical
fastboot flash boot boot-debug.subimg
fastboot reboot fastboot
fastboot flash system system.img
fastboot -w
fastboot reboot

#note: Don't lock until you flash to normal f/w

==========CTS-ON-GSI==========
fastboot flashing unlock
fastboot flashing unlock_critical
fastboot reboot fastboot
fastboot flash system system.img
fastboot -w
fastboot reboot bootloader
fastboot flashing lock 
fastboot flashing lock_critical
fastboot reboot