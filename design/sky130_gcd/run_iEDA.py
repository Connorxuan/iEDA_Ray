#!/bin/python3
from config import *
import os
import optuna
from lib import config
import sqlite3
import multiprocessing
import time
import shutil
import ray

pwd = os.getcwd()
foundry_dir = f'{pwd}/../../foundry/sky130'

def objective(trial):
    trial_dir = f"{pwd}/run_{trial.number}"
    os.makedirs(trial_dir, exist_ok=True)

    source_config_dir = f'{pwd}/iEDA_config'
    dest_config_dir = f'{trial_dir}/iEDA_config'
    if os.path.exists(dest_config_dir):
        shutil.rmtree(dest_config_dir)
    shutil.copytree(source_config_dir, dest_config_dir)

    source_result_dir = f'{pwd}/result'
    dest_result_dir = f'{trial_dir}/result'
    if os.path.exists(dest_result_dir):
        shutil.rmtree(dest_result_dir)
    shutil.copytree(source_result_dir, dest_result_dir)

    env_vars = {
        'DESIGN_TOP'    : 'gcd',
        'NETLIST_FILE'  : f'{pwd}/result/verilog/gcd.v',
        'SDC_FILE'      : f'{foundry_dir}/sdc/gcd.sdc',
        'SPEF_FILE'     : f'{foundry_dir}/spef/gcd.spef',
        'DIE_AREA'      : '0.0   0.0   149.96   150.128',
        'CORE_AREA'     : '9.996 10.08 139.964  140.048',
        'FOUNDRY_DIR'   : foundry_dir,
        'CONFIG_DIR'    : dest_config_dir,
        'RESULT_DIR'    : f'{trial_dir}/result',
        'TCL_SCRIPT_DIR': f'{pwd}/script',
    }

    max_fanout=trial.suggest_int("max_fanout",20,40)
    is_max_length_opt = 0 # trial.suggest_int("is_max_length_opt",0,1)
    max_length_constraint = trial.suggest_int("max_length_constraint", 900000,1100000)
    is_timing_effort = 0 #trial.suggest_int("is_timing_aware_mode",0,1)
    ignore_net_degree = trial.suggest_int("ignore_net_degree", 90,110)
    num_threads = 1 #trial.suggest_int("num_threads", 1, 64)
    init_wirelength_coef=trial.suggest_float("init_wirelength_coef",0.2,0.3)
    reference_hpwl=trial.suggest_int("reference_hpwl",440000000,450000000)
    min_wirelength_force_bar=trial.suggest_int("min_wirelength_force_bar",-400,-200 )
    target_density=trial.suggest_float("target_density", 0.5, 0.9) #
    bin_cnt_x=128 #trial.suggest_categorical("bin_cnt_x", [32, 64, 128, 256])
    bin_cnt_y=128 #trial.suggest_categorical("bin_cnt_y", [32, 64, 128, 256])
    max_iter=trial.suggest_int("max_iter",1000,3000)
    max_backtrack=trial.suggest_int("max_backtrack",5,15)
    init_density_penalty=0.00008 #trial.suggest_float("init_density_penalty",0.000001,0.0001) #
    target_overflow=trial.suggest_float("target_overflow",0.05,0.15)
    initial_prev_coordi_update_coef=trial.suggest_int("initial_prev_coordi_update_coef",90,110) #
    min_precondition=1.0 #trial.suggest_int("min_precondition",0.8,1.0)
    min_phi_coef=trial.suggest_float("min_phi_coef",0.9,1)
    max_phi_coef=trial.suggest_float("max_phi_coef",1,1.1)
    max_buffer_num=trial.suggest_int("max_buffer_num",900000,1100000)
    max_displacement=trial.suggest_int("max_displacement",900000,1100000)
    global_right_padding=trial.suggest_int("global_right_padding",0,1)
    config(max_fanout,is_max_length_opt,max_length_constraint,is_timing_effort,ignore_net_degree,num_threads,init_wirelength_coef,
        reference_hpwl,min_wirelength_force_bar,target_density,bin_cnt_x,bin_cnt_y,max_iter,max_backtrack,init_density_penalty,target_overflow,
        initial_prev_coordi_update_coef,min_precondition,min_phi_coef,max_phi_coef,max_buffer_num,max_displacement,global_right_padding,
        config_dir=dest_config_dir
        #read_cts_data,write_cts_data,router_type,delay_type,skew_bound,max_buf_tran,max_sink_tran,max_cap,max_fanout2,max_length,scale_size,
        #cluster_type,cluster_size,buffer_type,routing_layer_1,routing_layer_2,external_model,use_netlist,clock_name,net_name
    )
    ray.get(main.remote(env_vars))

    with open(f'{trial_dir}/result/cts/sta/gcd.rpt', 'r') as file:
        lines = file.readlines()
        if len(lines) >= 5:
            line = lines[5]
            symbols = line.split('|')
            if len(symbols) >= 8:
                latency = float(symbols[8].strip())
    with open(f'{trial_dir}/result/report/cts_db.rpt', 'r') as file:
        lines = file.readlines()
        if len(lines) >= 5:
            line = lines[20]
            symbols = line.split('|')
            if len(symbols) >= 2:
                area1 = symbols[2].strip()
                area2  = area1.split(' ')
                area = float(area2[0])
    return area,latency

@ray.remote(scheduling_strategy="DEFAULT")
def main(env_vars):
    os.chdir(pwd)
    set_environment_variables(env_vars)
    print("""
    #===========================================================
    ##   run floorplan"
    #===========================================================
    """)
    execute_shell_command('./iEDA -script ./script/iFP_script/run_iFP.tcl')

    print("""
    #===========================================================
    ##   run NO -- fix fanout
    #===========================================================
    """)
    execute_shell_command('./iEDA -script ./script/iNO_script/run_iNO_fix_fanout.tcl')

    print("""
    #===========================================================
    ##   run Placer
    #===========================================================
    """)
    execute_shell_command('./iEDA -script ./script/iPL_script/run_iPL.tcl')
    # execute_shell_command('./iEDA -script ./script/iPL_script/run_iPL_eval.tcl')

    print("""
    # ===========================================================
    #   run CTS
    # ===========================================================
    """)
    execute_shell_command('./iEDA -script ./script/iCTS_script/run_iCTS.tcl')
    # execute_shell_command('./iEDA -script ./script/iCTS_script/run_iCTS_eval.tcl')
    execute_shell_command('./iEDA -script ./script/iCTS_script/run_iCTS_STA.tcl')

    print("""
    #===========================================================
    ##   run TO -- fix_drv
    #===========================================================
    """)
    execute_shell_command('./iEDA -script ./script/iTO_script/run_iTO_drv.tcl')
    execute_shell_command('./iEDA -script ./script/iTO_script/run_iTO_drv_STA.tcl')

    print("""
    #===========================================================
    #   run TO -- opt_hold
    #===========================================================
    """)

    execute_shell_command('./iEDA -script ./script/iTO_script/run_iTO_hold.tcl')
    execute_shell_command('./iEDA -script ./script/iTO_script/run_iTO_hold_STA.tcl')

    print("""
    # ===========================================================
    # #   run TO -- opt_setup
    # ===========================================================
    """)

    # execute_shell_command('./iEDA -script ./script/iTO_script/run_iTO_setup.tcl')

    print("""
    #===========================================================
    #   run PL Incremental Flow
    #===========================================================
    """)

    execute_shell_command('./iEDA -script ./script/iPL_script/run_iPL_legalization.tcl')
    # execute_shell_command('./iEDA -script ./script/iPL_script/run_iPL_legalization_eval.tcl')

    print("""
    #===========================================================
    # #   run Router
    #===========================================================
    """)

    execute_shell_command('./iEDA -script ./script/iRT_script/run_iRT.tcl')
    # execute_shell_command('./iEDA -script ./script/iRT_script/run_iRT_eval.tcl')
    # execute_shell_command('./iEDA -script ./script/iRT_script/run_iRT_STA.tcl')
    execute_shell_command('./iEDA -script ./script/iRT_script/run_iRT_DRC.tcl')

    print("""
    #===========================================================
    ##   run DRC --- report
    #===========================================================
    """)
    # execute_shell_command('./iEDA -script ./script/iDRC_script/run_iDRC.tcl')

    print("""
    #===========================================================
    ##   run Filler
    #===========================================================
    """)

    execute_shell_command('./iEDA -script ./script/iPL_script/run_iPL_filler.tcl')

    print("""
    #===========================================================
    ##   run ECO
    #===========================================================
    """)

    print("""
    #===========================================================
    ##   run PV
    #===========================================================
    """)

    print("""
    #===========================================================
    ##   run def to gdsii
    #===========================================================
    """)

    execute_shell_command('./iEDA -script ./script/DB_script/run_def_to_gds_text.tcl')

if __name__ == "__main__":
    study = optuna.create_study(directions=["minimize", "minimize"],study_name="1222",storage="sqlite:///data.db",load_if_exists=True)
    def worker():
        study.optimize(objective, n_trials=1)

    num_processes = 1
    processes = []
    for _ in range(num_processes):
        process = multiprocessing.Process(target=worker)
        processes.append(process)

    start_time = time.time()
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    end_time = time.time()

    time_cost = end_time - start_time
    result_str = "Single-process serial REAL runtime(1st time): %.2f s" % time_cost
    with open('BaseDSEReport.txt', 'w') as file:
        file.write(result_str + '\n')
    print(result_str)

    time_predict = time_cost * 100
    result_str = "Single-process serial PREDICTION runtime(1st time):%.2f s" % time_predict
    with open('BaseDSEReport.txt', 'a') as file:
        file.write(result_str + '\n')
    print(result_str)

    # with open("ChipPilotReport.txt", "r") as file:
    #     first_line = file.readline().strip()
    #     parallel_cost = float(first_line.split("s")[1].strip()[:-1])
    # speed_up = time_cost2 / parallel_cost
    # result_str = "speedup: %.2f" % speed_up 
    # print(result_str)       
    # with open('BaseDSEReport.txt', 'a') as file2:
    #     file2.write(result_str + '\n')
