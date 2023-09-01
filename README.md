# Python SCPI for Rohde & Schwarz VNAs

Python SCPI script to collect complex-valued trace data from an R&S VNA. The scripts also allows disabling factory calibration.

The SCPI commands were taken from the user manual of the tested VNAs. Currently tested VNAs are:

- ZVA <https://www.rohde-schwarz.com/manual/zva/>
- ZNA <https://www.rohde-schwarz.com/manual/zna/>
- ZNL (to be updated)

## Code requirement

You need two packages installed in your python environment [`pyvisa`](https://pyvisa.readthedocs.io/en/latest/index.html) and [`numpy`](https://numpy.org/install/), both which can be installed as follows:

```powershell
python -m pip install -U pyvisa numpy
```

You also need to install a VISA [backend](https://pyvisa.readthedocs.io/en/latest/introduction/getting.html):

```powershell
python -m pip install -U pyvisa-py
```

You basically load the script for the desired VNA in your main script and start collecting data. For the example file [`example.py`](https://github.com/ZiadHatab/scpi-rohde-schwarz-vna/blob/main/example.py), please check its dependency directly in the file.

## Code snippet

You can collect complex-valued traces on the screen without changing any settings by using the code below. All you need to do is define the necessary settings on the VNA and collect data. In the script, you can specify the channel and number of sweeps to be collected. If you want to sweep different stimulus settings (or whatever settings), you can define each channel with different settings and sweep that channel.

```python
    import numpy as np
    
    # my code
    import zva as vna 
    # import zna as vna

    frequencies, measurements, trace_definitions = vna.read_traces(address='GPIB0::6::INSTR', num_sweeps=10, channels=[1])
    # trace_definitions gives the definition of the collected data in the same order as stored in the 'measurements' variable
    # the variable frequencies holds the frequency grid for each selected channel.
```