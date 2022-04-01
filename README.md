# Capacitor-DC-Bias-Characteristics
Script outputs a graph of capacitance over a DC range. Input a csv of of time and voltage. Implements a moving average (M).


Inputs
    CSV, each row is a list of [time, voltage]
    No headers or extra info
Outputs
    Apart from misc info about the data the main output is a graph displaying the capacitance over the range of voltages measured
        There is some loss either end due to data trimming and the moving average.
    The capacitance at 12V and 24V is calculated in the title, this has been relevant to my work at TDK on the DH modules for QM


Future
    Add latex support
    Make graph prettier
    Have the extra info, currently in the title, displayed elsewhere
    