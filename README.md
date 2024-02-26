<h1>LARS' USB SCANNER</h1>

<h2>INSTALLATION GUIDE:</h2>

1. RUN 'sudo apt update' | *This will update apt instance*
2. RUN 'sudo apt install git pip python usbutils udisks2 clamav clamav-daemon' | *Install required packages for this project*
3. RUN 'sudo service clamav-freshclam stop | *Will stop freshclam service if running*
4. RUN 'sudo freshclam' | *ClamAV virus database will be updated*
5. RUN 'sudo apt install clamtk' | *Install GUI for ClamAV*
6. RUN 'sudo git clone https://github.com/larsje99/usbscanner.git' | *Clone the repository into home directory*
7. RUN 'cd usbscanner_for_ParrotOS/usbscanner' | *Navigate to the folder*
8. RUN 'sudo mv usbscannerlars /usr/local/bin' | *Move the bash script to PATH environment*
9. RUN 'sudo chmod +x /usr/local/bin/usbscannerlars' | *Make the script executable*
10. RUN 'cd ../..' | *Go back to home directory*
11. RUN 'sudo usbscannerlars' | *Now you can run the script!*

VERSION 0.0.1
FUTURE UPDATES COMING SOON!
