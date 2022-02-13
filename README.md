# coral-inference-environment-on-64bitRaspberryPiOS
Procedure for building Coral USB Accelerator inference environment on 64bit Raspberry Pi OS.  

It is a memorandum of environment construction.  

<br>
<br>

## **Physical specifications**

#### **RaspberryPi**
Hardware: BCM2835  
Model: Raspberry Pi 4 Model B Rev 1.2  
microSD card: 32GB or more  

#### **Inference accelerator**
Coral USB Accelerator  

#### **USB camera**
logicool C270N  
<br>
<br />

## **Development environment**
#### **RaspberryPi**
Kernel: Linux    
Kernel release No.: 5.10.63-v8+   
Kernel version: #1459 SMP PREEMPT Wed Oct 6 16:42:49 BST 2021 aarch64    
OS： Raspbian GNU/Linux 10 (buster)  
Language: python 3.7.2  
<br/>

## **Construction procedure**

### **Preparation**
1.  Prepare RaspberryPi OS image disc.  https://www.raspberrypi.com/software/
2. Insert the OS image disc into the Raspberry Pi and turn on the power.
3. Make initial settings for Raspberry Pi, ssh/VNC available and connect to the Internet.  
4. Connect c270n to USB 2.0 port.  
<br>

### **Building an environment on Raspberry Pi**
Start Raspberry so that it can connect to VNC and connect to the Internet.  
  
Clone this project from public repository
```sh  
git clone https://github.com/nsaito9628/coral-inference-environment-on-64bitRaspberryPiOS.git
```
  
Deploy a project  
``` sh
cp ./coral-inference-environment-on-64bitRaspberryPiOS/*.sh ~
cp ./coral-inference-environment-on-64bitRaspberryPiOS/sample/* ~
```

Download and unpack the required packages.
```sh
sudo chmod u+x environment.sh
./environment.sh
```  
  
Insert Coral USB Accelerator to USB3.0 port.  
<br>

### **Confirmation of human detection operation**
```sh  
sudo python3 capture_detection_cv2.py --model ./mobilenet_ssd_v1_coco_quant_postprocess_edgetpu.tflite --label coco_labels.txt --keep_aspect_ratio --threshold 0.5
```
