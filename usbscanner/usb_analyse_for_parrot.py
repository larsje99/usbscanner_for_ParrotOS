def main():
    import subprocess
    import time
    import sys
    import os.path
    import os
    list_of_red_flags = ['Self Powered', 'Human Interface Device', 'Boot Interface Subclass', 'Keyboard', 'HID', 'bNumEndpoints           1', 'Interrupt']
    device_id = []
    
    def parse_usb_info(usb_info):
        list_of_important_fields = ['idVendor', 'idProduct', 'bmAttributes', 'Powered', 'bNumEndpoints', 'bInterfaceClass', 'bInterfaceSubClass', 'bInterfaceProtocol', 'HID', 'Endpoint Descriptor', 'bEndpointAddress', 'Transfer Type']
        list_of_flags = []
        lines = iter(usb_info.split('\n'))
        
        for line in lines:
            if line.startswith('Bus'):
                device = line
                confirmation = input("Do you want to analyze this device: " + "|" + device + "|" + "? " + "TYPE YES OR NO: ")
                if confirmation == "YES":
                    testing = device.split(' ')
                    code = testing[5]
                    device_id.append(code)
                    while True:
                        next_line = next(lines)
                        if next_line.startswith('Bus') or next_line == '':
                            print("\n")
                            break
                        for field in list_of_important_fields:
                            if field in next_line:
                                if field == 'idVendor':
                                    list_of_flags.append("\n-------------------------------------------------------------\n\n")
                                list_of_flags.append(next_line)
                                break
                    print("-----------------------------\n\033[1mDEVICE ANALYZED\033[0m\n-----------------------------\n\n")
                elif confirmation == "NO":
                    print("\n\n-----------------------------\n\033[1mSKIPPING TO NEXT DEVICE\033[0m\n-----------------------------\n\n")
                else:
                    print("\n\033[1mError, please input YES or NO\033[0m\n")

        return list_of_flags

    text = "LARS' BADUSB ANALYZER"
    box_width = len(text) + 4
    print("\n")
    print("*" * box_width)
    print("* {:^{}s} *".format(text, len(text)))
    print("*" * box_width)

    print("\n------------------------------------------------\n\033[1mALWAYS BE CRITICAL AND LOOK AT THE FULL REPORT!\033[0m\n------------------------------------------------\n")

    red_flags_counter = 0

    while True:
        input_choice = input("TYPE \'full\' FOR THE FULL USB REPORT, TYPE \'indiv\' FOR INDIVIDUAL USB ANALYSES: ")

        if input_choice == "full":
            lsusb_output = subprocess.run(['lsusb', '-v'], capture_output=True, text=True)

            if lsusb_output.returncode == 0:
                usb_info = lsusb_output.stdout
                print(usb_info)
                sys.exit()
                break
                
        elif input_choice == "indiv":
            lsusb_output = subprocess.run(['lsusb', '-v'], capture_output=True, text=True)

            if lsusb_output.returncode == 0:
                usb_info = lsusb_output.stdout
                print("\n")
                parsed_usb_info = parse_usb_info(usb_info)

                print("\n-----------------------------\n\033[1mRESULTS OF ANALYSES\033[0m\n-----------------------------\n↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓\n")
                for item in parsed_usb_info:
                    for red_flag in list_of_red_flags:
                        if red_flag in item:
                            red_flags_counter += 1
                    print(item)
            
                if red_flags_counter == 0:
                    text2 = "NO POTENTIAL RED FLAGS HAVE BEEN FOUND!"
                    box_width = len(text2) + 4
                    print("\n")
                    print("*" * box_width)
                    print("* {:^{}s} *".format(text2, len(text2)))
                    print("*" * box_width)
                    print("\n")
                    break
                elif red_flags_counter != 0:
                    text3 = str(red_flags_counter) + " POTENTIAL RED FLAGS DETECTED!"
                    box_width = len(text3) + 4
                    print("\n")
                    print("*" * box_width)
                    print("* {:^{}s} *".format(text3, len(text3)))
                    print("*" * box_width)
                    print("\n")
                    break
                    
            else:
                print("Error running lsusb command. Exit code:", lsusb_output.returncode)
                break
                
        else:
            print("\n-------------------------------------------------\nINVALID CHOICE, PLEASE CHOOSE \'full\' OR \'indiv\'\n-------------------------------------------------\n")
    
    print("********************************************************************************")
    time.sleep(3)
    
    # IMAGE MAKEN
    ## make directory to capture flash drive image
    
    image_of_drive_dir = 'image_of_drive'
    
    ## return flash drive path
    try:
        flash_drive_path = subprocess.getoutput(['lsscsi | rev | cut -d \' \' -f2 | rev'])
        list_of_paths = flash_drive_path.split('\n')
        cleaned_list = [x for x in list_of_paths if x != '']
    except:
        print("\033[1mERROR: UNABLE TO RETRIEVE FLASH DRIVE PATH, CHECK CONNECTIVITY OF FLASH DRIVE!\033[0m")
    
    image_making_confirm = input("DO YOU WANT TO CREATE A NEW IMAGE OR PROCEED WITH EXISTING IMAGE? TYPE \'CREATE\' or \'PROCEED\': ")
    
    if image_making_confirm == "CREATE":    
        print("\n")
        print("\033[1mIMAGE CREATION OF CONNECTED DRIVE WILL START!\033[0m \n\n")
        name_checker = True
        while name_checker == True:
            name_for_image = input("PLEASE ENTER A FILENAME FOR THE IMAGE: ")
            if os.path.exists(name_for_image + ".E01"):
                print("\n \033[1mERROR: FILE NAME ALREADY IN DIRECTORY!\033[0m \n")
                name_checker = True
            else:
                name_checker = False
                break
                
        image_command = 'sudo ewfacquire -w -m removable -l image_process_log -c fast -f ftk -t ' + str(name_for_image) + ' ' + cleaned_list[-1]
        subprocess.run(image_command, shell=True)
        print("\n\n-----------------------------\n\033[1mIMAGE SUCCESFULLY CREATED!\033[0m\n-----------------------------\n\n")
    
    elif image_making_confirm == "PROCEED":
        print("\n")
        name_for_image = input("PLEASE ENTER THE NAME OF EXISTING FILE WITHOUT EXTENSION (MUST BE IN HOME DIRECTORY): ") 
    else:
        print("\n \033[1mERROR: INVALID INPUT!\033[0m")
     
    # IMAGE MOUNTEN
    
    if os.path.exists('ewf_mount') and os.path.exists('logical_mount'):
        print("MOUNTING DIRECTORIES ALREADY EXIST")
    else:
        subprocess.run(['sudo', 'mkdir', 'ewf_mount'])
        subprocess.run(['sudo', 'mkdir', 'logical_mount'])
    
    subprocess.run(['sudo', 'ewfmount', name_for_image + '.E01', 'ewf_mount'])
    time.sleep(1)
    retrieve_mount_point = subprocess.getoutput('sudo ls -alh ewf_mount | rev | cut -d \' \' -f1 | rev | tail -n 1')
    time.sleep(1)
    mount_point_list = retrieve_mount_point.split("\n")
    logical_mount_command = subprocess.run('sudo mount -o ro ewf_mount/' + mount_point_list[-1] + ' logical_mount', shell=True)
    time.sleep(1)
    
    # IMAGE CONTENTS COPY PASTE IN HOME DIRECTORY
    
    if os.path.exists('map_to_scan'):
        print("SCAN DIRECTORY ALREADY EXISTS")
    else:
        subprocess.run(['sudo', 'mkdir', 'map_to_scan'])

    subprocess.run('sudo cp -r logical_mount/* map_to_scan', shell=True)
    
    # .E01 CONVERTEN NAAR .RAW
    
    print("\n\n---------------------------------------\n\033[1mCREATING ADDITIONAL .RAW IMAGE FOR CARVING...\033[0m\n---------------------------------------\n\n")
    time.sleep(2)
    
    subprocess.run('sudo ewfexport -u ' + name_for_image + '.E01 ' + '-t converted_' + name_for_image, shell=True)
    
    # .RAW BESTAND CARVEN OP HIDDEN FILES
    
    if os.path.exists('recovered_files'):
        print("RECOVER DIRECTORY ALREADY EXISTS")
    else:
        subprocess.run(['sudo', 'mkdir', 'recovered_files'])
        
    print("\n\n---------------------------------------\n\033[1mCARVING PROCESS STARTING...\033[0m\n---------------------------------------\n\n")    
    time.sleep(2)
    
    try:
        subprocess.run('sudo scalpel -o recovered_files converted_' + name_for_image + '.raw -v', shell=True)
        print("\n SUCCES \n")
    except:
        print("\n ERROR: SOMETHING WENT WRONG \n")
    
    # MOVE CARVED TO SCAN MAP
    
    subprocess.run('sudo mv recovered_files map_to_scan', shell=True)
    
    # SCAN MAP IN HOME DIRECTORY
    
    print("\n\n-----------------------------\n\033[1mVIRUS SCANNER WILL NOW OPEN\033[0m\n-----------------------------\n\n")
    time.sleep(2)
    subprocess.run(['clamtk'])   
    
    # MOVE CREATED IMAGE TO FINAL FOLDER
    
    subprocess.run(['sudo', 'mkdir', 'drive_E01_image'])
    subprocess.run('sudo mv ' + name_for_image + '.E01 drive_E01_image', shell=True)
    time.sleep(1)
    subprocess.run('sudo mv drive_E01_image map_to_scan', shell=True)
    
    # ZIP MAP FOR FINAL USE
    
    subprocess.run('sudo zip -r final_folder.zip map_to_scan/*', shell=True)
    
    #CLEAN UP
    
    subprocess.run("sudo rm -r map_to_scan/*", shell=True)
    subprocess.run("sudo rm converted_" + name_for_image + ".raw")
    subprocess.run("sudo umount logical_mount", shell=True)
    subprocess.run("sudo umount ewf_mount", shell=True)
    
    print("\n\n---------------------------------------\n\033[1mALL FILES MOVED TO: final_folder.zip\033[0m\n---------------------------------------\n\n")    
    time.sleep(2)
    
if __name__ == "__main__":
    main()
