import subprocess

class Data:
  def __init__(self, direct, periodic):
    self.direct = direct
    self.periodic = periodic

def run_sim(class_talents, spec_talents, apl, sim_file, spell_name):
    # replace apl with one provided from base sim file
    base = open(f"internal/sim_files/{sim_file}", "rt")
    out = open (f"internal/sim_files/out.simc", "wt")

    for line in base:
        new_line = line
        new_line = new_line.replace("${apl}", apl)
        new_line = new_line.replace("${class_talents}", class_talents)
        new_line = new_line.replace("${spec_talents}", spec_talents)
        out.write(new_line)

    base.close()
    out.close()

    subprocess.run(["../../simc/simc.exe", f"internal/sim_files/out.simc", "output=internal/sim_files/output.txt"])
    return analyze_sim( spell_name )

def analyze_sim(spell_name):
    simOutput = []
    direct_list = []
    periodic_list = []

    with open(r"internal/sim_files/output.txt", 'r') as file:
        simOutput = file.readlines()
        file.close()

    for line in simOutput:
        if f'direct amount for Action {spell_name}' in line:
            amount = float(line.split()[8].split('=')[1].strip())
            direct_list.append(amount)
        if f'tick amount for Action {spell_name}' in line:
            amount = float(line.split()[12].split('=')[1].strip())
            periodic_list.append(amount)
    return Data(direct_list, periodic_list)