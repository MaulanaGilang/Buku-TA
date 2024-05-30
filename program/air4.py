import os
import random

def generate_airgap_cylinders(file, box_height):
    # Define bounds for airgap cylinder placement
    x_min, x_max = 0.05, 0.95
    y_min, y_max = 0.090, box_height - 0.05  # Adjusted Y bounds to ensure cylinders are within the concrete slab
    
    airgap_count = random.randint(1, 2)  # Generate 1 or 2 airgaps per file
    for _ in range(airgap_count):
        # Each airgap formed by 3 to 5 cylinders
        cylinder_count = random.randint(3, 5)
        
        # Initial positions for the first cylinder in an airgap
        x_position = random.uniform(x_min, x_max)
        y_position = random.uniform(y_min, y_max)

        for _ in range(cylinder_count):
            radius = random.uniform(0.010, 0.035) / 2  # Radius between 0.010m and 0.035m
            # Write cylinder, then adjust positions for the next one
            file.write(f"#cylinder: {x_position:.3f} {y_position:.3f} 0.0 {x_position:.3f} {y_position:.3f} 0.001 {radius:.3f} free_space\n")
            
            # Tighten adjustments for X and Y to encourage collisions
            x_adjust = random.uniform(-0.010, 0.010)
            y_adjust = random.uniform(-0.010, 0.010)
            
            # Update positions ensuring they remain within defined bounds
            x_position = min(max(x_position + x_adjust, x_min), x_max)
            y_position = min(max(y_position + y_adjust, y_min), y_max)

def generate_gprMax_files():
    base_content = """#title: B-scan from rebar in concrete

#domain: 1.0 0.3 0.001
#dx_dy_dz: 0.001 0.001 0.001
#time_window: 3e-9

#material: 7.0 0.0 1.0 0.0 concrete
#material: 12.0 1.0e6 1.0 0.0 steel

#waveform: ricker 1 4.5e9 my_ricker
#src_steps: 0.001 0 0
#rx_steps: 0.001 0 0
"""

    parent_folder = "airgap"
    os.makedirs(parent_folder, exist_ok=True)

    box_height_start = 0.190
    box_height_end = 0.210
    total_files = 2000  # Adjust total files generated to 2000

    for file_number in range(1, total_files + 1):
        box_height = random.uniform(box_height_start, box_height_end)
        folder_name = os.path.join(parent_folder, str(file_number))
        os.makedirs(folder_name, exist_ok=True)
        filename = os.path.join(folder_name, f"data{file_number}.in")

        with open(filename, "w") as file:
            file.write(base_content)
            file.write(f"#box: 0.0 0.0 0.0 1.0 {box_height:.3f} 0.001 concrete\n")
            file.write(f"#hertzian_dipole: z 0.010 {box_height:.3f} 0 my_ricker\n")
            file.write(f"#rx: 0.050 {box_height:.3f} 0\n")

            # Generate steel cylinders with a common Y position
            common_y_position = random.uniform(0.090, 0.110)  # Fixed Y position for steel cylinders within the range
            for position in [0.050, 0.200, 0.350, 0.500, 0.650, 0.800, 0.950]:
                new_x = (position + (file_number * 0.001)) % 1.0
                file.write(f"#cylinder: {new_x:.3f} {common_y_position:.3f} 0.0 {new_x:.3f} {common_y_position:.3f} 0.001 0.007 steel\n")

            # Generate abstract airgap shapes with tightened X and Y adjustments
            generate_airgap_cylinders(file, box_height)

            print(f"Generated file: {folder_name}/data{file_number}.in")

generate_gprMax_files()
