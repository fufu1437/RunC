"""
通过编辑配置文件来快速运行c代码的脚本
"""

import json
import os
import re
import subprocess

RunCConfig = {
    "main_Nmae_And_Path":"",
    "main_Output_Path":"",

    "pack_Name_And_Path":{
    }
}

def main():
    Calibration = False
    include = []
    try:
        f = open("RunCConfig.json","r")
        config = json.load(f)
        f.close()
    except FileNotFoundError:
        with open("RunCConfig.json","w",encoding='utf-8') as f:
            json.dump(RunCConfig ,f, indent=4)
        return 

    main_Nmae_And_Path = config["main_Nmae_And_Path"]
    pack_Name_And_Path = config["pack_Name_And_Path"]

    if re.search("/",main_Nmae_And_Path):
        mainName = main_Nmae_And_Path[re.search("/",main_Nmae_And_Path).end():-2] # type: ignore

    else:
        mainName = main_Nmae_And_Path[:-2]

    mainF = open(main_Nmae_And_Path,"r",encoding='utf-8')

    for mainRead in mainF:
        if re.search("#include",mainRead):
            include.append(mainRead[8:-2].strip().strip("\"")[:-2])

    mainF.close()
    mainOutputPath = config["main_Output_Path"]
    code =  f"gcc {main_Nmae_And_Path} "
    for name ,path in pack_Name_And_Path.items():
        Calibration = True
        if name[:-2] in include:
            code = f"{code} {path}/{name} -I{path} -o {mainOutputPath}/{mainName}.exe"
        else:
            code = f"{code} -o {mainOutputPath}/{mainName}.exe"
    if not Calibration:
        if mainOutputPath.strip() == "":
            code = f"{code} -o {mainName}.exe"
        else:
            code = f"{code} -o {mainOutputPath}/{mainName}.exe"
    os.system(code)
    print(f"Success: Compiled to {mainName}.c\n")
    if mainOutputPath.strip() != "":
        mainRunCode = f"./{mainOutputPath}/{mainName}.exe"
    else:
        mainRunCode = f"./{mainName}.exe"
    
    subprocess.run([mainRunCode])
    print("\nRun End")
main()