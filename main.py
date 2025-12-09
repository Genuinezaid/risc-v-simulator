import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from simulator import RISCVSimulator

class RISCVSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RISC-V 5-Stage Pipeline Simulator")
        self.root.geometry("1400x900")

        self.simulator = RISCVSimulator()
        self.speed_ms = 500

        self.setup_ui()
        self.update_displays()

        sample_code = """# Sample RISC-V Program with Hazards
addi x1, x0, 10
addi x2, x0, 20
add x3, x1, x2
sub x4, x3, x1
sw x4, 0(x0)
lw x5, 0(x0)
addi x6, x5, 5
beq x3, x3, 8
addi x7, x0, 100"""
        self.code_text.insert('1.0', sample_code)

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        header = ttk.Label(main_frame, text="RISC-V 5-Stage Pipeline Simulator",
                          font=('Arial', 16, 'bold'))
        header.grid(row=0, column=0, columnspan=2, pady=10)

        left_frame = ttk.LabelFrame(main_frame, text="Assembly Code (RV32I)", padding="10")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)

        self.code_text = scrolledtext.ScrolledText(left_frame, width=40, height=20,
                                                  font=('Courier', 10))
        self.code_text.pack(fill=tk.BOTH, expand=True)

        control_frame = ttk.Frame(left_frame)
        control_frame.pack(fill=tk.X, pady=5)

        ttk.Button(control_frame, text="Load Program",
                  command=self.load_program).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Run",
                  command=self.run_program).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Step",
                  command=self.step_program).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Reset",
                  command=self.reset_simulator).pack(side=tk.LEFT, padx=2)

        speed_frame = ttk.Frame(left_frame)
        speed_frame.pack(fill=tk.X, pady=5)
        ttk.Label(speed_frame, text="Speed (ms):").pack(side=tk.LEFT)
        self.speed_var = tk.IntVar(value=500)
        speed_scale = ttk.Scale(speed_frame, from_=100, to=2000,
                               variable=self.speed_var, orient=tk.HORIZONTAL,
                               command=self.update_speed)
        speed_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.speed_label = ttk.Label(speed_frame, text="500ms")
        self.speed_label.pack(side=tk.LEFT)

        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        right_frame.rowconfigure(0, weight=0)
        right_frame.rowconfigure(1, weight=1)
        right_frame.rowconfigure(2, weight=0)
        right_frame.columnconfigure(0, weight=1)

        pipeline_frame = ttk.LabelFrame(right_frame, text="Pipeline Stages", padding="10")
        pipeline_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)

        self.cycle_label = ttk.Label(pipeline_frame, text="Cycle: 0",
                                    font=('Arial', 12, 'bold'))
        self.cycle_label.pack()

        stages_frame = ttk.Frame(pipeline_frame)
        stages_frame.pack(fill=tk.X, pady=5)

        self.stage_labels = {}
        stage_names = ['IF', 'ID', 'EX', 'MEM', 'WB']
        stage_full = ['Fetch', 'Decode', 'Execute', 'Memory', 'Write Back']

        for i, (stage, full) in enumerate(zip(stage_names, stage_full)):
            frame = ttk.LabelFrame(stages_frame, text=f"{stage} ({full})", padding="5")
            frame.grid(row=0, column=i, padx=2, sticky=(tk.W, tk.E, tk.N, tk.S))
            stages_frame.columnconfigure(i, weight=1)

            label = ttk.Label(frame, text="Empty", font=('Courier', 9),
                            justify=tk.LEFT, wraplength=150)
            label.pack()
            self.stage_labels[stage] = label

        notebook = ttk.Notebook(right_frame)
        notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        reg_frame = ttk.Frame(notebook, padding="10")
        notebook.add(reg_frame, text="Registers")

        reg_canvas = tk.Canvas(reg_frame)
        reg_scrollbar = ttk.Scrollbar(reg_frame, orient="vertical", command=reg_canvas.yview)
        self.reg_inner_frame = ttk.Frame(reg_canvas)

        self.reg_inner_frame.bind("<Configure>",
                                 lambda e: reg_canvas.configure(scrollregion=reg_canvas.bbox("all")))

        reg_canvas.create_window((0, 0), window=self.reg_inner_frame, anchor="nw")
        reg_canvas.configure(yscrollcommand=reg_scrollbar.set)

        reg_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        reg_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.register_labels = []
        for i in range(32):
            frame = ttk.Frame(self.reg_inner_frame, relief=tk.RIDGE, borderwidth=1, padding="5")
            frame.grid(row=i//4, column=i%4, padx=2, pady=2, sticky=(tk.W, tk.E))

            ttk.Label(frame, text=f"x{i}", font=('Courier', 9, 'bold')).pack()
            label = ttk.Label(frame, text="0", font=('Courier', 9))
            label.pack()
            self.register_labels.append(label)

        mem_frame = ttk.Frame(notebook, padding="10")
        notebook.add(mem_frame, text="Memory")

        mem_canvas = tk.Canvas(mem_frame)
        mem_scrollbar = ttk.Scrollbar(mem_frame, orient="vertical", command=mem_canvas.yview)
        self.mem_inner_frame = ttk.Frame(mem_canvas)

        self.mem_inner_frame.bind("<Configure>",
                                 lambda e: mem_canvas.configure(scrollregion=mem_canvas.bbox("all")))

        mem_canvas.create_window((0, 0), window=self.mem_inner_frame, anchor="nw")
        mem_canvas.configure(yscrollcommand=mem_scrollbar.set)

        mem_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        mem_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.memory_labels = []
        for i in range(64):
            frame = ttk.Frame(self.mem_inner_frame, relief=tk.RIDGE, borderwidth=1, padding="3")
            frame.grid(row=i//4, column=i%4, padx=2, pady=2, sticky=(tk.W, tk.E))

            label = ttk.Label(frame, text=f"[{i}]: 0", font=('Courier', 8))
            label.pack()
            self.memory_labels.append(label)

        inst_frame = ttk.Frame(notebook, padding="10")
        notebook.add(inst_frame, text="Instructions")

        self.inst_tree = ttk.Treeview(inst_frame, columns=('PC', 'Instruction', 'Type'),
                                     show='headings', height=15)
        self.inst_tree.heading('PC', text='PC')
        self.inst_tree.heading('Instruction', text='Instruction')
        self.inst_tree.heading('Type', text='Type')
        self.inst_tree.column('PC', width=50)
        self.inst_tree.column('Instruction', width=200)
        self.inst_tree.column('Type', width=50)

        inst_scrollbar = ttk.Scrollbar(inst_frame, orient="vertical", command=self.inst_tree.yview)
        self.inst_tree.configure(yscrollcommand=inst_scrollbar.set)

        self.inst_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        inst_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        stats_frame = ttk.LabelFrame(right_frame, text="Statistics & Hazard Detection", padding="10")
        stats_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)

        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill=tk.X)

        self.total_cycles_label = ttk.Label(stats_grid, text="Total Cycles: 0", font=('Arial', 10))
        self.total_cycles_label.grid(row=0, column=0, padx=10, pady=2, sticky=tk.W)

        self.inst_exec_label = ttk.Label(stats_grid, text="Instructions Executed: 0", font=('Arial', 10))
        self.inst_exec_label.grid(row=0, column=1, padx=10, pady=2, sticky=tk.W)

        self.hazards_label = ttk.Label(stats_grid, text="Hazards Detected: 0", font=('Arial', 10))
        self.hazards_label.grid(row=1, column=0, padx=10, pady=2, sticky=tk.W)

        self.cpi_label = ttk.Label(stats_grid, text="CPI: 0.00", font=('Arial', 10))
        self.cpi_label.grid(row=1, column=1, padx=10, pady=2, sticky=tk.W)

        log_label = ttk.Label(stats_frame, text="Execution Log:", font=('Arial', 9, 'bold'))
        log_label.pack(anchor=tk.W, pady=(5, 0))

        self.log_text = scrolledtext.ScrolledText(stats_frame, height=8, font=('Courier', 8))
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def update_speed(self, value):
        self.speed_ms = int(float(value))
        self.speed_label.config(text=f"{self.speed_ms}ms")

    def load_program(self):
        code = self.code_text.get('1.0', tk.END)
        count = self.simulator.load_program(code)
        messagebox.showinfo("Load Program", f"Loaded {count} instructions")
        self.reset_simulator()
        self.update_instruction_table()

    def step_program(self):
        if self.simulator.step():
            self.update_displays()
        else:
            messagebox.showinfo("Execution", "Program execution completed")

    def run_program(self):
        if self.simulator.cpu.is_running:
            self.simulator.cpu.is_running = False
            if hasattr(self.simulator.cpu, 'run_after_id') and self.simulator.cpu.run_after_id:
                self.root.after_cancel(self.simulator.cpu.run_after_id)
            return

        self.simulator.cpu.is_running = True
        self.run_step()

    def run_step(self):
        if self.simulator.cpu.is_running:
            if self.simulator.step():
                self.update_displays()
                self.simulator.cpu.run_after_id = self.root.after(self.speed_ms, self.run_step)
            else:
                self.simulator.cpu.is_running = False
                messagebox.showinfo("Execution", "Program execution completed")

    def reset_simulator(self):
        if hasattr(self.simulator.cpu, 'run_after_id') and self.simulator.cpu.run_after_id:
            self.root.after_cancel(self.simulator.cpu.run_after_id)
        self.simulator.cpu.is_running = False
        self.simulator.reset()
        self.update_displays()
        self.log_text.delete('1.0', tk.END)

    def update_displays(self):
        self.cycle_label.config(text=f"Cycle: {self.simulator.cycle}")

        for stage in ['IF', 'ID', 'EX', 'MEM', 'WB']:
            pipe_stage = self.simulator.pipeline[stage]
            if pipe_stage.get('instruction'):
                inst = pipe_stage['instruction']
                text = f"{inst['raw']}\n"
                if stage == 'ID':
                    text += f"rs1: x{inst.get('rs1', 0)}\nrs2: x{inst.get('rs2', 0)}\nrd: x{inst.get('rd', 0)}"
                elif stage == 'EX':
                    text += f"Result: {pipe_stage.get('aluResult', 0)}"
                elif stage == 'MEM':
                    text += f"Data: {pipe_stage.get('data', 0)}"
                elif stage == 'WB':
                    text += f"rd: x{pipe_stage.get('rd', 0)}\nData: {pipe_stage.get('data', 0)}"
                self.stage_labels[stage].config(text=text)
            else:
                self.stage_labels[stage].config(text="Bubble")

        for i, label in enumerate(self.register_labels):
            label.config(text=str(self.simulator.registers[i]))

        for i, label in enumerate(self.memory_labels):
            label.config(text=f"[{i}]: {self.simulator.memory_values[i]}")

        self.total_cycles_label.config(text=f"Total Cycles: {self.simulator.cycle}")
        self.inst_exec_label.config(text=f"Instructions Executed: {self.simulator.instructions_executed}")
        self.hazards_label.config(text=f"Hazards Detected: {self.simulator.hazards_detected}")
        self.cpi_label.config(text=f"CPI: {self.simulator.get_cpi():.2f}")

        if len(self.simulator.execution_log) > 0:
            last_log = self.simulator.execution_log[-1]
            log_entry = f"[Cycle {last_log['cycle']}] {last_log['message']}\n"
            self.log_text.insert(tk.END, log_entry)
            self.log_text.see(tk.END)

    def update_instruction_table(self):
        for item in self.inst_tree.get_children():
            self.inst_tree.delete(item)

        for idx, inst in enumerate(self.simulator.instructions):
            self.inst_tree.insert('', tk.END, values=(idx * 4, inst['raw'], inst['type']))


def main():
    root = tk.Tk()
    app = RISCVSimulatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()