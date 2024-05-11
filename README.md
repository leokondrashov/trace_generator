# Invitro Trace Generator

Offers finer control over the generation of traces for the Invitro experiment:
1. Number of functions
2. Invocation step size
3. Stagger duration between functions
4. Intermediate step proportion
5. Stabilisation period
6. Function execution duration
7. Wait duration between invocations (of the same function)

| Settings                      | Default Value | Explanation                                                                                           |
| ----------------------------- | ------------- | ----------------------------------------------------------------------------------------------------- |
| functions                     | -             | Number of functions deployed in the experiment                                                        |
| invocation                    | -             | Invocation step size                                                                                  |
| stagger                       | 5             | Time interval between invocations of different functions                                              |
| proportion                    | 0             | Intermediate step value as a proportion of the invocation step, used with `stabilisation` and `wait`  |
| stabilisation                 | 0             | Number of repetitions to stabilise the invocation pattern, used with `proportion` and `wait`          |
| wait                          | 5             | Time interval between invocations of the same function, used with `proportion` and `stabilisation`    |
| execution                     | 1000          | Execution time of the functions in ms                                                                 |
| memory                        | 1024          | Memory usage of the functions in MB                                                                   |
| output                        | -             | Output path for the resulting trace                                                                   |


## Difference from [Invitro's Trace Synthesizer Tool](https://github.com/vhive-serverless/invitro/tree/main/tools/trace_synthesizer)
1. Offers finer control over the generation of traces

    | Comparison                    | Invitro Trace Synthesizer | Invitro Trace Generator |
    | ----------------------------- | ------------------------- | ----------------------- |
    | Time Unit Assumed             | RPM (see `mode 0`)        | Flexible (e.g. RPS or RPM is based on experiment's `config.json`) |
    | Duration Generated            | 24 hours (1,440 time unit)| Flexible, based on input settings (able to generate beyond 1,440 and under 1,440 time unit) |
    | Invocation Size and Pattern   | Required to manually edit code (e.g. `mode 1`, `mode 2` uses invocation size 1 and fixed paddings)   | Flexible, based on CLI arguments |

2. Specifically supports the generation of the same synthetic traces used in my Final Year Project experiments

    | Experiment                                    | Main Variables To Change       |
    | --------------------------------------------- | ------------------------------ |
    | Stagger Duration Between Functions            | `stagger`                      |
    | Function Execution Duration                   | `execution`                    |
    | Number of Deployed Functions                  | `functions`                    |
    | Invocation Step Size (Scaling from Zero)      | `invocation`                   |
    | Invocation Step Size (Scaling from Non-Zero)  | `proportion`, `stabilisation`  |
    | Keep Alive Policy                             | `wait`                         |


## Sample Reference to Generate Traces
The following are sample Bash commands used to generate traces for the AWS Invitro experiment, as described in my Final Year Project report [here](https://dr.ntu.edu.sg/handle/10356/175344).

> Note: For my FYP project, the time granularity used is in seconds, not minutes. The time granularity can be changed in the `config.json` file before running Invitro.

### Generate Experiment Trace for Stagger Duration Between Functions
```bash
python . generate -f 10 -i 100 -stag 1 -e 1000 -o stagger_duration_experiment/stagger_1
python . generate -f 10 -i 100 -stag 5 -e 1000 -o stagger_duration_experiment/stagger_5
python . generate -f 10 -i 100 -stag 15 -e 1000 -o stagger_duration_experiment/stagger_15
```

### Generate Experiment Trace for Function Execution Duration
```bash
python . generate -f 10 -i 100 -stag 5 -e 1000 -o execution_duration_experiment/execution_1
python . generate -f 10 -i 100 -stag 5 -e 5000 -o execution_duration_experiment/execution_5
python . generate -f 10 -i 100 -stag 5 -e 15000 -o execution_duration_experiment/execution_15
```

### Generate Experiment Trace for Number of Deployed Functions
```bash
python . generate -f 10 -i 10 -stag 5 -e 1000 -o deployed_funcs_experiment/funcs_10
python . generate -f 50 -i 10 -stag 5 -e 1000 -o deployed_funcs_experiment/funcs_50
python . generate -f 100 -i 10 -stag 5 -e 1000 -o deployed_funcs_experiment/funcs_100
```

### Generate Experiment Trace for Invocation Step Size (Scaling from Zero)
```bash
python . generate -f 10 -i 10 -stag 5 -e 1000 -o invocation_step_zero_scaling_experiment/invocation_10
python . generate -f 10 -i 50 -stag 5 -e 1000 -o invocation_step_zero_scaling_experiment/invocation_50
python . generate -f 10 -i 100 -stag 5 -e 1000 -o invocation_step_zero_scaling_experiment/invocation_100
```

### Generate Experiment Trace for Invocation Step Size (Scaling from Non-Zero)
```bash
python . generate -f 10 -i 10 -stag 5 -p 0.1 -stab 1 -w 5 -e 1000 -o invocation_step_nonzero_scaling_experiment/proportion_10_stabilisation_1
python . generate -f 10 -i 10 -stag 5 -p 0.5 -stab 1 -w 5 -e 1000 -o invocation_step_nonzero_scaling_experiment/proportion_50_stabilisation_1
python . generate -f 10 -i 10 -stag 5 -p 0.1 -stab 3 -w 5 -e 1000 -o invocation_step_nonzero_scaling_experiment/proportion_10_stabilisation_3
python . generate -f 10 -i 10 -stag 5 -p 0.5 -stab 3 -w 5 -e 1000 -o invocation_step_nonzero_scaling_experiment/proportion_50_stabilisation_3
```

### Generate Experiment Trace for Keep Alive Policy
```bash
python . generate -f 1 -i 100 -p 1 -stab 9 -w 60 -e 1000 -o keep_alive_policy_experiment/keep_alive_60
python . generate -f 1 -i 100 -p 1 -stab 9 -w 120 -e 1000 -o keep_alive_policy_experiment/keep_alive_120
python . generate -f 1 -i 100 -p 1 -stab 9 -w 180 -e 1000 -o keep_alive_policy_experiment/keep_alive_180
```