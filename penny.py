import tkinter as tk
from math import cos, sin, radians, degrees, atan2, sqrt, acos
import serial
import time

# === Serial Port Setup ===
COM_PORT = 'COM12'
BAUD_RATE = 9600

try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
except serial.SerialException:
    print(f"Failed to open serial port {COM_PORT}")
    ser = None

# === Link lengths (in mm) ===
L1 = 120 
L2 = 220    

# === Shoulder offset and elbow inversion ===
SHOULDER_OFFSET = 55

# === Forward Kinematics ===
def compute_fk():
    joint_theta0 = radians(slider_vars[0].get())
    joint_theta1 = radians(slider_vars[1].get())
    joint_theta2 = radians(slider_vars[2].get())

    reach = L1 * cos(joint_theta1) + L2 * cos(joint_theta2)
    x = reach * cos(joint_theta0)
    y = reach * sin(joint_theta0)
    z = L1 * sin(joint_theta1) + L2 * sin(joint_theta2)

    x_val.set(f"X: {x:.2f} mm")
    y_val.set(f"Y: {y:.2f} mm")
    z_val.set(f"Z: {z:.2f} mm")

    send_angles(joint_theta1, joint_theta2)

# === Send Angles to Arduino ===
def send_angles(joint_theta1, joint_theta2):
    if ser and ser.is_open:
        servo_theta1 = degrees(joint_theta1) + SHOULDER_OFFSET
        servo_theta2 = 180 - degrees(joint_theta2)  # Invert elbow

        angles = [slider_vars[0].get(), servo_theta1, servo_theta2,
                  slider_vars[3].get(), slider_vars[4].get(), slider_vars[5].get(),
                  brush_var.get(), pump_var.get()]  # Append m and n

        data = ",".join(map(str, angles)) + "\n"
        ser.write(data.encode())

        # ✅ Print what is being sent
        print(f"Sending to Arduino: {data.strip()}")

# === Reset Function ===
def reset_all():
    for var in slider_vars:
        var.set(90)
    compute_fk()

# === Inverse Kinematics ===
def inverse_kinematics():
    try:
        x_in = float(x_entry.get())
        y_in = float(y_entry.get())
        z_in = float(z_entry.get())

        # Base angle
        theta0 = atan2(y_in, x_in)

        # Project into XZ plane
        r = sqrt(x_in**2 + y_in**2)
        x = r
        z = z_in

        dist = sqrt(x**2 + z**2)
        if dist > (L1 + L2):
            raise ValueError("Target out of reach.")

        # Law of cosines for elbow (relative angle)
        cos_theta2_rel = (x**2 + z**2 - L1**2 - L2**2) / (2 * L1 * L2)
        cos_theta2_rel = max(min(cos_theta2_rel, 1), -1)
        theta2_rel = acos(cos_theta2_rel)

        # Shoulder angle
        phi = atan2(z, x)
        beta = atan2(L2 * sin(theta2_rel), L1 + L2 * cos(theta2_rel))
        theta1 = phi - beta

        # Elbow absolute angle
        theta2 = theta1 + theta2_rel

        # Update sliders
        slider_vars[0].set(int(degrees(theta0)))
        slider_vars[1].set(int(degrees(theta1)))
        slider_vars[2].set(int(degrees(theta2)))

        compute_fk()  # Update FK display and send to Arduino

    except Exception as e:
        print(f"IK Error: {e}")

# === GUI Setup ===
root = tk.Tk()
root.title("6-DOF Arm Control")

slider_vars = [tk.IntVar(value=90) for _ in range(6)]
labels = ["Base", "Shoulder (Joint)", "Elbow (Joint)", "Wrist Roll", "Wrist Pitch", "Gripper"]

for i, label in enumerate(labels):
    tk.Label(root, text=label).grid(row=i, column=0, padx=10, pady=5)
    max_val = 90 if label == "Gripper" else 180
    tk.Scale(root, from_=0, to=max_val, orient='horizontal',
             variable=slider_vars[i],
             command=lambda val: compute_fk()
             ).grid(row=i, column=1, padx=10, pady=5)

# === Display FK ===
x_val = tk.StringVar()
y_val = tk.StringVar()
z_val = tk.StringVar()
tk.Label(root, textvariable=x_val, font=("Arial", 12)).grid(row=6, column=0, columnspan=2, pady=5)
tk.Label(root, textvariable=y_val, font=("Arial", 12)).grid(row=7, column=0, columnspan=2, pady=5)
tk.Label(root, textvariable=z_val, font=("Arial", 12)).grid(row=8, column=0, columnspan=2, pady=5)

# === Reset Button ===
tk.Button(root, text="Reset", command=reset_all, bg="lightblue").grid(row=9, column=0, columnspan=2, pady=10)

# === Inverse Kinematics Inputs ===
tk.Label(root, text="X:").grid(row=10, column=0)
x_entry = tk.Entry(root)
x_entry.grid(row=10, column=1)

tk.Label(root, text="Y:").grid(row=11, column=0)
y_entry = tk.Entry(root)
y_entry.grid(row=11, column=1)

tk.Label(root, text="Z:").grid(row=12, column=0)
z_entry = tk.Entry(root)
z_entry.grid(row=12, column=1)

# === IK Send Button ===
tk.Button(root, text="Send IK", command=inverse_kinematics, bg="orange").grid(row=13, column=0, columnspan=2, pady=10)


brush_var = tk.IntVar(value=0)
pump_var = tk.IntVar(value=0)

def toggle_brush():
    compute_fk()  # Just send updated state, do not flip brush_var manually

def toggle_pump():
    compute_fk()


tk.Checkbutton(root, text="Brush", variable=brush_var, command=toggle_brush).grid(row=14, column=0, pady=5)
tk.Checkbutton(root, text="Pump", variable=pump_var, command=toggle_pump).grid(row=14, column=1, pady=5)


# === Initial Display ===
compute_fk()

# === GUI Main Loop ===
root.mainloop()

# === Close Serial on Exit ===
if ser and ser.is_open:
    ser.close()
