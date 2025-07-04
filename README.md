# Penultimate – 6DOF Robotic Arm

**Penultimate** is a desktop-scale 6DOF robotic arm designed for precision control and real-time interaction. Built using standard-sized servos and a custom end effector, the project features full inverse and forward kinematics, a Python GUI interface, and modular Arduino firmware. 

This arm is intended for educational and research applications in robotics, embedded systems, and automation control.

---

## 🔩 Features

- 6 Degrees of Freedom + Gripper (SG90 roll configuration)
- Real-time control via a custom-built Python GUI
- Custom inverse and forward kinematics (no external libraries)
- Modular firmware written in Arduino C++
- Clean CAD layout with replaceable end effector design
- Targeted for desktop use with cost-effective components

---

## 🧠 Technologies Used

- **Microcontroller**: Arduino UNO
- **Programming**: C++ (Arduino), Python (math, serial, GUI)
- **Servos**: OT5325M digital servos, SG90 for gripper
- **Tools**: EasyEDA, SolidWorks / Fusion 360
- **Kinematics**: Pure trigonometric computation (no IK libraries)

## 📸 Preview

![Penultimate Robotic Arm](images/penultimate_full.jpg)

_Optional: Add images of GUI, gripper, or motion demo here._

---

## 🚧 Current Status

✅ Complete: Mechanical build, firmware, GUI  
🛠 In Progress: Modular IK solver improvements, feedback loop (future)  
📦 Planned: Integration with ROS or serial visualisation tools

---

## 📚 Acknowledgement

The mechanical layout of this project was initially inspired by the **HowToMechatronics 6DOF Arduino Robotic Arm**.  
However, this version significantly diverges from the original with:

- A completely custom **Python GUI** for real-time control
- Fully implemented **inverse and forward kinematics**
- Use of PCA9685 Servo Driver
- Freshly written **Arduino firmware**
- Modified **servo setup** and **end effector**
- A modular structure suited for further research and development

This is an independent, portfolio-focused project built from the ground up.

---

## 📬 Contact

For queries, collaboration, or demo requests, feel free to reach out:

**Sendhan S**  
📧 sendhan007@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/sendhan-s-2483a3274/)  
