import logging
import os
import pandas as pd

from utils import load_data, save_data, hash_generator

def generate(args):
    sampleCount = 1

    logging.basicConfig(filename='synthesizer.log', level=logging.DEBUG, force=True)
    inv_df = load_data("./base_traces/inv.csv")
    mem_df = load_data("./base_traces/mem.csv")
    run_df = load_data("./base_traces/run.csv")

    # Generate the hashes for function, owner and app
    lenHashes = 64
    hashFunction = [hash_generator(lenHashes) for _ in range(args.num_of_funcs)]
    hashOwner = [hash_generator(lenHashes) for _ in range(args.num_of_funcs)]
    hashApp = [hash_generator(lenHashes) for _ in range(args.num_of_funcs)]

    # =================== Generating inv.csv ===================
    # Compute total duration required for experiment
    experiment_duration = args.num_of_funcs * (args.wait_duration * args.stabilisation_count + args.stagger_duration) - args.stagger_duration + 1

    # Initialise the invocation pattern table with 0 and the corresponding headers
    inv = pd.DataFrame([[0] * experiment_duration] * args.num_of_funcs, columns=list(range(1, experiment_duration+1)))

    # Populate the invocation pattern table with the intermediate and final step values
    for i in range(args.num_of_funcs):
        # Obtain the intermediate step value
        invocation_intermediate_step = args.invocation_step * args.intermediate_step_proportion

        # Generate the index of intermediate step values, if any
        intermediate_idx = []
        for j in range(args.stabilisation_count):
            intermediate_idx.append(i*(args.wait_duration * args.stabilisation_count + args.stagger_duration) + j*args.wait_duration)

        # Generate the index of the final step value
        if intermediate_idx:
            final_idx = intermediate_idx[-1] + args.wait_duration
        else:
            final_idx = i * args.stagger_duration

        # Populate the invocation pattern accordingly
        inv.iloc[i, intermediate_idx] = invocation_intermediate_step
        inv.iloc[i, final_idx:final_idx+1] = args.invocation_step
    
    inv_df["HashApp"] = hashApp
    inv_df["HashFunction"] = hashFunction
    inv_df["HashOwner"] = hashOwner
    inv_df = pd.concat([inv_df, inv], axis=1)

    # =================== Generating mem.csv ===================
    for i in range(args.num_of_funcs):
        mem_df.loc[i] = [hashApp[i], hashFunction[i], hashOwner[i], sampleCount] + [args.memory] * (len(mem_df.columns) - 4)


    # =================== Generating run.csv ===================
    for i in range(args.num_of_funcs):
        run_df.loc[i] = [hashApp[i], hashFunction[i], hashOwner[i], args.execution_duration, sampleCount] + [args.execution_duration] * (len(run_df.columns) - 5)


    # =================== Save generated files ===================
    save_data(inv_df, f"{args.output_path}/invocations.csv")
    save_data(mem_df, f"{args.output_path}/memory.csv")
    save_data(run_df, f"{args.output_path}/durations.csv")

    return inv_df, mem_df, run_df