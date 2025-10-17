import os
def change_config_no_fix_out(key,value,directory):
    new_content = ""
    with open(directory, 'r') as f:
        content = f.readlines()
    for i in content:
        if str(key) in str(i) :
            new_item = str(key) + str(value)
            print(new_item)
            new_content = new_content + str(new_item) + "\n"
        else :
            new_content = new_content + str(i)
    with open(directory, 'w') as f_new:
        f_new.write(new_content)

def change_config_pl(key,value,directory):
    new_content = ""
    with open(directory, 'r') as f:
        content = f.readlines()
    for i in content:
        if str(key) in str(i) :
            new_item = str(key) + str(value) + ","
            print(new_item)
            new_content = new_content + str(new_item) + "\n"
        else :
            new_content = new_content + str(i)
    with open(directory, 'w') as f_new:
        f_new.write(new_content)

def change_config_pl_end(key,value,directory):
    new_content = ""
    with open(directory, 'r') as f:
        content = f.readlines()
    for i in content:
        if str(key) in str(i) :
            new_item = str(key) + str(value) 
            print(new_item)
            new_content = new_content + str(new_item) + "\n"
        else :
            new_content = new_content + str(i)
    with open(directory, 'w') as f_new:
        f_new.write(new_content)

def change_config_pl_str(key,value,directory):
    new_content = ""
    with open(directory, 'r') as f:
        content = f.readlines()
    for i in content:
        if str(key) in str(i) :
            new_item = str(key) + str(value) + "\","
            print(new_item)
            new_content = new_content + str(new_item) + "\n"
        else :
            new_content = new_content + str(i)
    with open(directory, 'w') as f_new:
        f_new.write(new_content)

def change_config_cts_str(key,value,directory):
    new_content = ""
    with open(directory, 'r') as f:
        content = f.readlines()
    for i in content:
        if str(key) in str(i) :
            new_item = str(key) + str(value) + "\","
            print(new_item)
            new_content = new_content + str(new_item) + "\n"
        else :
            new_content = new_content + str(i)
    with open(directory, 'w') as f_new:
        f_new.write(new_content)

def change_config_cts(key,value,directory):
    new_content = ""
    with open(directory, 'r') as f:
        content = f.readlines()
    for i in content:
        if str(key) in str(i) :
            new_item = str(key) + str(value) + "\","
            print(new_item)
            new_content = new_content + str(new_item) + "\n"
        else :
            new_content = new_content + str(i)
    with open(directory, 'w') as f_new:
        f_new.write(new_content)

def change_config_cts_nostr(key,value,directory):
    new_content = ""
    with open(directory, 'r') as f:
        content = f.readlines()
    for i in content:
        if str(key) in str(i) :
            new_item = str(key) + str(value) + ","
            print(new_item)
            new_content = new_content + str(new_item) + "\n"
        else :
            new_content = new_content + str(i)
    with open(directory, 'w') as f_new:
        f_new.write(new_content)

def change_config_buffer_type(key,value,directory):
    config_dir = f'{directory}/..'
    if key=="buffer_type":
        with open(directory, 'r') as f:
            content = f.readlines()
        if len(content) == 0:
            # 读取文件2
            with open(f'{config_dir}/cts_default_config2.json', 'r') as file2:
                content2 = file2.read()
            # 写入文件1
            with open(f'{config_dir}/cts_default_config.json', 'w') as file1:
                file1.write(content2)
            # 读取文件2
            with open(f'{config_dir}/pl_default_config2.json', 'r') as file4:
                content3 = file4.read()
            # 写入文件1
            with open(f'{config_dir}/pl_default_config.json', 'w') as file3:
                file3.write(content3)
        else:
            content[21] = '        \"' + str(value) + '\"\n'
            with open(directory, 'w') as f_new:
                f_new.writelines(content)

def change_config_routing_layer(key,value,directory):
    if key=="routing_layer_1":
        with open(directory, 'r') as f:
            content = f.readlines()
        if len(content)>24:
            content[24] = '        ' + str(value) + ',\n'
            with open(directory, 'w') as f_new:
                f_new.writelines(content)
    if key=="routing_layer_2":
        with open(directory, 'r') as f:
            content = f.readlines()
        if len(content)>24:
            content[25] = '        ' + str(value) + '\n'
            with open(directory, 'w') as f_new:
                f_new.writelines(content)

def config(max_fanout,is_max_length_opt,max_length_constraint,is_timing_aware_mode,ignore_net_degree,num_threads,init_wirelength_coef,
    reference_hpwl,min_wirelength_force_bar,target_density,bin_cnt_x,bin_cnt_y,max_iter,max_backtrack,init_density_penalty,target_overflow,
    initial_prev_coordi_update_coef,min_precondition,min_phi_coef,max_phi_coef,max_buffer_num,max_displacement,global_right_padding,
    solution_type,perturb_per_step,cool_rate,parts,ufactor,new_macro_density,halo_x,halo_y,read_cts_data,write_cts_data,router_type,
    delay_type,skew_bound,max_buf_tran,max_sink_tran,max_cap,max_fanout2,max_length,scale_size,cluster_type,cluster_size,buffer_type,
    routing_layer_1,routing_layer_2,external_model,use_netlist,clock_name,net_name):

    pwd = os.getcwd()
    config_dir = f'{pwd}/../iEDA_config'

    change_config_no_fix_out('    \"max_fanout\": ',max_fanout,f'{config_dir}/no_default_config_fixfanout.json')

    change_config_pl('        \"is_max_length_opt\": ',is_max_length_opt,f'{config_dir}/pl_default_config.json')
    change_config_pl('        \"max_length_constraint\": ',max_length_constraint,f'{config_dir}/pl_default_config.json')
    change_config_pl('        \"is_timing_aware_mode\": ',is_timing_aware_mode,f'{config_dir}/pl_default_config.json')
    change_config_pl('        \"ignore_net_degree\": ',ignore_net_degree,f'{config_dir}/pl_default_config.json')
    change_config_pl('        \"num_threads\": ',num_threads,f'{config_dir}/pl_default_config.json')
    change_config_pl('                \"init_wirelength_coef\": ',init_wirelength_coef,f'{config_dir}/pl_default_config.json')
    change_config_pl('                \"reference_hpwl\": ',reference_hpwl,f'{config_dir}/pl_default_config.json')
    change_config_pl_end('                \"min_wirelength_force_bar\": ',min_wirelength_force_bar,f'{config_dir}/pl_default_config.json')
    change_config_pl('                \"target_density\": ',target_density,f'{config_dir}/pl_default_config.json')
    change_config_pl('                \"bin_cnt_x\": ',bin_cnt_x,f'{config_dir}/pl_default_config.json')
    change_config_pl_end('                \"bin_cnt_y\": ',bin_cnt_y,f'{config_dir}/pl_default_config.json')
    change_config_pl('                \"max_iter\": ',max_iter,f'{config_dir}/pl_default_config.json')
    change_config_pl('                \"max_backtrack\": ',max_backtrack,f'{config_dir}/pl_default_config.json')
    change_config_pl('                \"init_density_penalty\": ',init_density_penalty,f'{config_dir}/pl_default_config.json')
    change_config_pl('                \"target_overflow\": ',target_overflow,f'{config_dir}/pl_default_config.json')
    change_config_pl('                \"initial_prev_coordi_update_coef\": ',initial_prev_coordi_update_coef,f'{config_dir}/pl_default_config.json')
    change_config_pl('                \"min_precondition\": ',min_precondition,f'{config_dir}/pl_default_config.json')
    change_config_pl('                \"min_phi_coef\": ',min_phi_coef,f'{config_dir}/pl_default_config.json')
    change_config_pl_end('                \"max_phi_coef\": ',max_phi_coef,f'{config_dir}/pl_default_config.json')
    change_config_pl('            \"max_buffer_num\": ',max_buffer_num,f'{config_dir}/pl_default_config.json')
    change_config_pl('            \"max_displacement\": ',max_displacement,f'{config_dir}/pl_default_config.json')
    change_config_pl_end('            \"global_right_padding\": ',global_right_padding,f'{config_dir}/pl_default_config.json')
    change_config_pl_str('            \"solution_type\": \"',solution_type,f'{config_dir}/pl_default_config.json')
    change_config_pl('                \"perturb_per_step\": ',perturb_per_step,f'{config_dir}/pl_default_config.json')
    change_config_pl_end('                \"cool_rate\": ',cool_rate,f'{config_dir}/pl_default_config.json')
    change_config_pl('                \"parts\": ',parts,f'{config_dir}/pl_default_config.json')
    change_config_pl('                \"ufactor\": ',ufactor,f'{config_dir}/pl_default_config.json')
    change_config_pl_end('                \"new_macro_density\": ',new_macro_density,f'{config_dir}/pl_default_config.json')
    change_config_pl('            \"halo_x\": ',halo_x,f'{config_dir}/pl_default_config.json')
    change_config_pl('            \"halo_y\": ',halo_y,f'{config_dir}/pl_default_config.json')

    change_config_cts('        \"read_cts_data\": \"',read_cts_data,f'{config_dir}/cts_default_config.json')
    change_config_cts('        \"write_cts_data\": \"',write_cts_data,f'{config_dir}/cts_default_config.json')
    change_config_cts('    \"router_type\": \"',router_type,f'{config_dir}/cts_default_config.json')
    change_config_cts('    \"delay_type\": \"',delay_type,f'{config_dir}/cts_default_config.json')
    change_config_cts('    \"skew_bound\": \"',skew_bound,f'{config_dir}/cts_default_config.json')
    change_config_cts('    \"max_buf_tran\": \"',max_buf_tran,f'{config_dir}/cts_default_config.json')
    change_config_cts('    \"max_sink_tran\": \"',max_sink_tran,f'{config_dir}/cts_default_config.json')
    change_config_cts('    \"max_cap\": \"',max_cap,f'{config_dir}/cts_default_config.json')
    change_config_cts('    \"max_fanout\": \"',max_fanout2,f'{config_dir}/cts_default_config.json')
    change_config_cts('    \"max_length\": \"',max_length,f'{config_dir}/cts_default_config.json')
    change_config_cts_nostr('    \"scale_size\": ',scale_size,f'{config_dir}/cts_default_config.json')
    change_config_cts('    \"cluster_type\": \"',cluster_type,f'{config_dir}/cts_default_config.json')
    change_config_cts_nostr('    \"cluster_size\": ',cluster_size,f'{config_dir}/cts_default_config.json')
    change_config_cts('    \"external_model\": \"',external_model,f'{config_dir}/cts_default_config.json')
    change_config_buffer_type("buffer_type",buffer_type,f'{config_dir}/cts_default_config.json')
    change_config_routing_layer("routing_layer_1",routing_layer_1,f'{config_dir}/cts_default_config.json')
    change_config_routing_layer("routing_layer_2",routing_layer_2,f'{config_dir}/cts_default_config.json')

    return
