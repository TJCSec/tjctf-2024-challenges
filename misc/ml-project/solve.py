import torch
import numpy as np
import z3

flag_len = 26

# load the model
class Model(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.f1 = torch.nn.Linear(flag_len, 22, dtype=torch.float64)
        self.relu = torch.nn.ReLU()
        self.f2 = torch.nn.Linear(22, 18, dtype=torch.float64)

    def forward(self, x):
        return self.f2(self.relu(self.f1(x)))

model = Model()

model.load_state_dict(torch.load("bin/model.pth"))

y = torch.load("bin/output.pth").detach().numpy()[0]
y = y.round().astype(np.int32)

weights1 = model.f1.weight.detach().numpy()
bias1 = model.f1.bias.detach().numpy()
weights2 = model.f2.weight.detach().numpy()
bias2 = model.f2.bias.detach().numpy()

# convert above parameters to integers
weights1 = weights1.round().astype(np.int32)
bias1 = bias1.round().astype(np.int32)
weights2 = weights2.round().astype(np.int32)
bias2 = bias2.round().astype(np.int32)

z3_x = np.array([z3.Int(f"x{i}") for i in range(flag_len)])

s = z3.Solver()
for z3_x_i, x_i in zip(z3_x, "tjctf{"):
    s.add(z3_x_i == ord(x_i))

for z3_x_i in z3_x:
    s.add(z3_x_i < 128)

s.add(z3_x[-1] == ord("}"))

z3_a1 = [z3.Int(f"a1_{i}") for i in range(25)]

for i in range(len(weights1)):
    s.add(z3_a1[i] == z3.Sum([a * int(b) for a, b in zip(z3_x, weights1[i])]) + int(bias1[i]))

z3_o = [z3.Int(f"o_{i}") for i in range(25)]

for i in range(len(weights2)):
    s.add(int(y[i]) == z3.Sum([a * int(b) for a, b in zip(z3_a1, weights2[i])]) + int(bias2[i]))

if s.check() != z3.sat:
    print("unsat")
    exit()

m = s.model()

print(m)

print("".join([chr(m[z3_x_i].as_long()) for z3_x_i in z3_x]))
